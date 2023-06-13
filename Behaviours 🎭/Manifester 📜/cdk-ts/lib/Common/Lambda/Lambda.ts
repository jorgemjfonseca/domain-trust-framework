import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as events from 'aws-cdk-lib/aws-events';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as s3n from 'aws-cdk-lib/aws-s3-notifications'


export class LAMBDA extends lambda.Function {

    Name: string;
    Role: iam.Role;

    constructor(scope: cdk.Stack , id: string, 
      dlq: sqs.Queue,
      props: cdk.aws_lambda.FunctionProps) {
        super(scope, id, {
          ...props,
          role: new iam.Role(scope, id+'FnRole', {
            assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com')
          }),
          functionName: scope+id,
          deadLetterQueue: dlq
        });

        this.Name = scope+id;

        this.Role = this.role as iam.Role;
        this.Role.addManagedPolicy(
          iam.ManagedPolicy.fromManagedPolicyArn(this, "AWSLambdaBasicExecutionRole", 
            'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'));

        dlq.grantSendMessages(this);
    }
    

    //https://github.com/aws-samples/serverless-patterns/blob/main/s3-lambda-dynamodb-cdk/cdk/lib/s3-lambda-dynamodb-cdk-stack.ts
    ConsumeEventsFromS3(bucket: s3.Bucket): LAMBDA {
      
      const lambdaRolePolicy = this.Role.assumeRolePolicy;
      
      lambdaRolePolicy?.addStatements(new iam.PolicyStatement({
        principals: [new iam.ServicePrincipal('s3.amazonaws.com')],
        actions: ['sts:AssumeRole']
      }));
      
      this.Role.addManagedPolicy(
        iam.ManagedPolicy.fromManagedPolicyArn(this, "AmazonS3ReadOnlyAccess", 
          'arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'));
      
      this.grantInvoke(new iam.ServicePrincipal('s3.amazonaws.com').withConditions({
        ArnLike: {
          'aws:SourceArn': bucket.bucketArn,
        },
        StringEquals: {
          'aws:SourceAccount': cdk.Aws.ACCOUNT_ID,
        }
      }));

      var destination = new s3n.LambdaDestination(this);
      var prefix = 'DomainManifest.yaml'; 
      bucket.addEventNotification(s3.EventType.OBJECT_CREATED, destination, { prefix: prefix });
      bucket.addEventNotification(s3.EventType.OBJECT_REMOVED, destination, { prefix: prefix });

      return this;
    }


    ConsumeMessagesFrom(queue: sqs.Queue): LAMBDA {
      queue.grantConsumeMessages(this);

      new lambda.EventSourceMapping(this, this.Name + 'Mapping', {
        eventSourceArn: queue.queueArn,
        target: this,
        batchSize: 1
      });

      return this;
    }

    SendMessagesToQueue(queue: sqs.Queue): LAMBDA {
      queue.grantSendMessages(this);
      return this;
    }

    SendMessagesToBus(bus: events.IEventBus): LAMBDA {
      bus.grantPutEventsTo(this);
      return this;
    }

}

