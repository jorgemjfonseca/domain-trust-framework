import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as events from 'aws-cdk-lib/aws-events';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as s3n from 'aws-cdk-lib/aws-s3-notifications'
import * as targets from 'aws-cdk-lib/aws-events-targets';
import { KEY } from '../KmsKey/KmsKey';
import { BUS } from '../EventBus/EventBus';
import { DLQ, QUEUE } from '../Queue/Queue';
import { S3 } from '../S3/S3';

export class LAMBDA  {

    Name: string;
    Role: iam.Role;
    Scope: cdk.Stack;
    Super: lambda.IFunction;

    constructor(scope: cdk.Stack, sup: lambda.IFunction)
    {
        this.Scope = scope;
        this.Super = sup;
        this.Name = sup.functionName;
        this.Role = sup.role as iam.Role
    }

    public static New(
      scope: cdk.Stack, 
      id: string, 
      props?: cdk.aws_lambda.FunctionProps
    ): LAMBDA {

        const dlq = DLQ.New(scope, id + "Dlq");
      
        const sup = new lambda.Function(scope, id, {
          role: new iam.Role(scope, id+'FnRole', {
            assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com')
          }),

          functionName: scope.stackName + id,
          deadLetterQueue: dlq.Super,
          memorySize: 1024, 
          timeout: cdk.Duration.seconds(30),

          ...props,

          runtime: props?.runtime 
            ?? lambda.Runtime.NODEJS_18_X,
          code: props?.code 
            ?? lambda.Code.fromAsset('lib/' + scope.stackName + '/lambda/' + id),
          handler: props?.handler 
            ?? 'exports.handler',
        });

        const fn = new LAMBDA(scope, sup);

        fn.Role.addManagedPolicy(
          iam.ManagedPolicy.fromManagedPolicyArn(scope, 
            fn.Super.functionName + "BasicExecutionRole", 
            'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'));

        dlq.Super.grantSendMessages(fn.Super);

        return fn;
    }

    public static FromFunctionName(scope: cdk.Stack, name: string) {
      return lambda.Function
        .fromFunctionName(scope, name, name);
    }
    

    // Exports to a CloudFormation parameter.
    public Export(alias: string): LAMBDA {
      new cdk.CfnOutput(this.Super, alias, {
        value: this.Super.functionName,
        exportName: alias,
      });
      return this;
    }

    // Imports from a CloudFormation parameter.
    public static Import(scope: cdk.Stack, alias: string): LAMBDA {
      const name = cdk.Fn.importValue(alias);
      const sup = lambda.Function.fromFunctionName(scope, alias, name);
      const ret = new LAMBDA(scope, sup);
      return ret;
    }


    //https://github.com/aws-samples/serverless-patterns/blob/main/s3-lambda-dynamodb-cdk/cdk/lib/s3-lambda-dynamodb-cdk-stack.ts
    public TriggeredByS3(bucket: S3): LAMBDA {
      
      const lambdaRolePolicy = this.Role.assumeRolePolicy;
      
      lambdaRolePolicy?.addStatements(new iam.PolicyStatement({
        principals: [new iam.ServicePrincipal('s3.amazonaws.com')],
        actions: ['sts:AssumeRole']
      }));
      
      this.Role.addManagedPolicy(
        iam.ManagedPolicy.fromManagedPolicyArn(this.Scope, "AmazonS3ReadOnlyAccess", 
          'arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'));
      
      this.Super.grantInvoke(new iam.ServicePrincipal('s3.amazonaws.com').withConditions({
        ArnLike: {
          'aws:SourceArn': bucket.Super.bucketArn,
        },
        StringEquals: {
          'aws:SourceAccount': cdk.Aws.ACCOUNT_ID,
        }
      }));

      var destination = new s3n.LambdaDestination(this.Super);
      var prefix = 'DomainManifest.yaml'; 
      bucket.Super.addEventNotification(s3.EventType.OBJECT_CREATED, destination, { prefix: prefix });
      bucket.Super.addEventNotification(s3.EventType.OBJECT_REMOVED, destination, { prefix: prefix });

      return this;
    }


    public TriggeredByQueue(queue: QUEUE): LAMBDA {
      queue.Super.grantConsumeMessages(this.Super);

      new lambda.EventSourceMapping(this.Scope, this.Name + 'Mapping', {
        eventSourceArn: queue.Super.queueArn,
        target: this.Super,
        batchSize: 1
      });

      return this;
    }


    public TriggeredByEventBus(
      eventBus: BUS,
      eventPattern: events.EventPattern,     //e.g. { source: ["DTFW"] }
      dlq: DLQ, 
      props?: targets.LambdaFunctionProps): LAMBDA 
    {
      const name = this.Super.functionName + eventBus.Super.eventBusName + 'Rule';
      
      const eventRule = new events.Rule(this.Scope, name, {
        ruleName: this.Scope.stackName + name,
        eventBus: eventBus.Super,
        eventPattern: eventPattern
      });

      eventRule.addTarget(
        new targets.LambdaFunction(this.Super, {
          deadLetterQueue: dlq.Super,
          maxEventAge: cdk.Duration.hours(2),
          retryAttempts: 2,
          ...props,
        }));

      return this;
    }


    public SendsMessagesToQueue(queue: QUEUE): LAMBDA {
      queue.Super.grantSendMessages(this.Super);
      return this;
    }

    public SendsMessagesToBus(bus: BUS): LAMBDA {
      bus.Super.grantPutEventsTo(this.Super);
      return this;
    }

    public SignsWithKey(key: KEY): LAMBDA {
      key.Super.grantEncrypt(this.Super);
      return this;
    }



}

