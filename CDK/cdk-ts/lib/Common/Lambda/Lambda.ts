import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as events from 'aws-cdk-lib/aws-events';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as s3n from 'aws-cdk-lib/aws-s3-notifications'
import * as sources from "aws-cdk-lib/aws-lambda-event-sources";
import * as targets from 'aws-cdk-lib/aws-events-targets';
import { KEY } from '../KEY/KEY';
import { BUS } from '../BUS/BUS';
import { DLQ, SQS } from '../SQS/SQS';
import { S3 } from '../S3/S3';
import { WORKFLOW } from '../WORKFLOW/WORKFLOW';
import { API } from '../API/API';
import { DYNAMO } from '../DYNAMO/DYNAMO';
import { NEPTUNE } from '../NEPTUNE/NEPTUNE';
import * as path from 'path';
import { STACK } from '../STACK/STACK';

export class LAMBDA {

    Name: string;
    Role: iam.Role;
    Scope: STACK;
    Super: lambda.Function;

    constructor(scope: STACK, sup: lambda.Function)
    {
        this.Scope = scope;
        this.Super = sup;
        this.Name = sup.functionName;
        this.Role = sup.role as iam.Role
    }

    public static New(
      scope: STACK, 
      id: string, 
      props?: cdk.aws_lambda.FunctionProps
    ): LAMBDA {

        const dlq = DLQ.New(scope, id + "Dlq");
      
        const role = new iam.Role(scope, id+'Role', {
          assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com')
        });

        role.addManagedPolicy(
          iam.ManagedPolicy.fromManagedPolicyArn(scope, 
            scope.Name + id + "BasicExecutionRole", 
            'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'));

        const sup = new lambda.Function(scope, id, {
          role: role,

          functionName: scope.Name + id,
          deadLetterQueue: dlq.Super,
          memorySize: 1024, 
          timeout: cdk.Duration.seconds(30),

          ...props,

          runtime: props?.runtime 
            ?? lambda.Runtime.NODEJS_18_X,
          code: props?.code 
            ?? lambda.Code.fromAsset(path.join(this.callerDirname(), '../lambda/' + id)),
          handler: props?.handler 
            ?? 'exports.handler',
        });

        const fn = new LAMBDA(scope, sup);

        dlq.Super.grantSendMessages(fn.Super);

        return fn;
    }

    private static callerDirname({ depth = 1 } = {}): string {
      if (typeof depth !== 'number' || depth < 1 || Math.floor(depth) !== depth)
        throw new Error('Depth must be a positive integer.');
    
      /* Start borrowed/modified code */
      // https://github.com/sindresorhus/callsites/blob/master/index.js
      const _ = Error.prepareStackTrace;
      Error.prepareStackTrace = (_, stack) => stack;
      const stack = new Error().stack!.slice(1);
      Error.prepareStackTrace = _;
    
      // https://github.com/sindresorhus/caller-callsite/blob/master/index.js
      const caller = (stack as any)
        .find((c: NodeJS.CallSite) => 
          //c.getTypeName() !== null &&
          path.dirname(c.getFileName()+'').includes('stack'));
      /* End borrowed/modified code */
    
      return path.dirname(caller.getFileName());
    }

    public static FromFunctionName(scope: STACK, name: string) {
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
    public static Import(scope: STACK, alias: string): LAMBDA {
      const name = cdk.Fn.importValue(alias);
      const sup = lambda.Function.fromFunctionName(scope, alias, name);
      const ret = new LAMBDA(scope, sup as lambda.Function);
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


    public TriggeredByQueue(queue: SQS): LAMBDA {
      queue.Super.grantConsumeMessages(this.Super);

      new lambda.EventSourceMapping(this.Scope, 'Mapping' + this.Scope.Next(), {
        eventSourceArn: queue.Super.queueArn,
        target: this.Super,
        batchSize: 1
      });

      return this;
    }


    public SpeaksWithBus(
      eventBus: BUS,
      // e.g. { source: ["DTFW"], detailType: ["CREATE", "UPDATE", "DELETE"] }
      source: string,
      detailType?: string[],
      props?: targets.LambdaFunctionProps): LAMBDA 
    {
      this.TriggeredByBus(eventBus, source, detailType, props);
      this.PublishesToBus(eventBus);
      return this;
    }


    public TriggeredByBus(
      eventBus: BUS,
      // e.g. { source: ["DTFW"], detailType: ["CREATE", "UPDATE", "DELETE"] }
      source: string,
      detailType?: string[],
      props?: targets.LambdaFunctionProps): LAMBDA 
    {
      const name = this.Name + eventBus.Name + 'Rule';
      
      const eventRule = new events.Rule(this.Scope, source+'Rule', {
        ruleName: this.Scope.Name + name,
        eventBus: eventBus.Super,
        eventPattern: {
          source: [ source ],
          detailType: detailType
        }
      });

      const dlq = DLQ.New(this.Scope, source + "ByBus");

      eventRule.addTarget(
        new targets.LambdaFunction(this.Super, {
          deadLetterQueue: dlq.Super,
          maxEventAge: cdk.Duration.hours(2),
          retryAttempts: 2,
          ...props,
        }));

      return this;
    }


    //https://docs.dennisokeeffe.com/aws-cdk/dynamodb-stream
    //https://serverlessland.com/patterns/dynamodb-streams-lambda-dynamodb-cdk-dotnet
    public TriggeredByDynamoDB(dynamo: DYNAMO): LAMBDA {
      dynamo.Super.grantStreamRead(this.Super);
      this.Super.addEventSource(
        new sources.DynamoEventSource(
          dynamo.Super, {
            startingPosition: lambda.StartingPosition.LATEST
          }
        ));
        return this;
    }


    public PublishesToQueue(queue: SQS): LAMBDA {
      queue.Super.grantSendMessages(this.Super);
      this.Super.addEnvironment("QUEUE_NAME", queue.Super.queueName);
      return this;
    }


    public PublishesToBus(bus: BUS): LAMBDA {
      bus.Super.grantPutEventsTo(this.Super);
      this.Super.addEnvironment("BUS_NAME", bus.Super.eventBusName);
      return this;
    }

    public SignsWithKey(key: KEY): LAMBDA {
      key.Super.grantEncrypt(this.Super);
      this.Super.addEnvironment("KEY_ARN", key.Super.keyArn);
      return this;
    }

    public WritesToS3(s3: S3): LAMBDA {
      s3.Super.grantReadWrite(this.Super);
      s3.Super.grantDelete(this.Super);
      s3.Super.grantPut(this.Super);
      this.Super.addEnvironment("S3_NAME", s3.Super.bucketName);
      return this;
    }

    public WritesToDynamoDBs(dynamos: DYNAMO[]): LAMBDA {
      dynamos.forEach(dynamo => {
        this.WritesToDynamoDB(dynamo);
      });
      return this;
    }

    public WritesToDynamoDB(dynamo: DYNAMO): LAMBDA {
      dynamo.Super.grantReadWriteData(this.Super);
      //dynamo.Super.grantStreamRead(this.Super);
      this.Super?.addEnvironment("TABLE_", dynamo.Super.tableName);
      return this;
    }

    public ReadsFromDynamoDBs(dynamos: DYNAMO[]): LAMBDA {
      dynamos.forEach(dynamo => {
        this.ReadsFromDynamoDB(dynamo);
      });
      return this;
    }

    public ReadsFromDynamoDB(dynamo: DYNAMO): LAMBDA {
      dynamo.Super.grantReadData(this.Super);
      //dynamo.Super.grantStreamRead(this.Super);
      if (this.Super.addEnvironment)
        this.Super.addEnvironment("TABLE_", dynamo.Super.tableName);
      return this;
    }


    public WritesToNeptune(neptune: NEPTUNE): LAMBDA {
      neptune.Super.grant(this.Super);
      neptune.Super.grantConnect(this.Super);
      this.Super.addEnvironment("NEPTUNE_HOSTNAME", neptune.Super.clusterEndpoint.hostname);
      this.Super.addEnvironment("NEPTUNE_PORT", neptune.Super.clusterEndpoint.port.toString());
      return this;
    }

    public ReadsFromNeptune(neptune: NEPTUNE): LAMBDA {
      neptune.Super.grant(this.Super);
      neptune.Super.grantConnect(this.Super);
      this.Super.addEnvironment("NEPTUNE_HOSTNAME", neptune.Super.clusterEndpoint.hostname);
      this.Super.addEnvironment("NEPTUNE_PORT", neptune.Super.clusterEndpoint.port.toString());
      return this;
    }


    public TriggersWorkflow(wf: WORKFLOW): LAMBDA {
      wf.Super.grantRead(this.Super);
      wf.Super.grantStartExecution(this.Super);
      wf.Super.grantStartSyncExecution(this.Super);
      wf.Super.grantTaskResponse(this.Super);
      this.Super.addEnvironment("WORKFLOW_ARN", wf.Super.stateMachineArn);
      return this;
    }


    public AddApiMethod(api: API, name: string, method: string = "POST"): LAMBDA {
      api.SendToLambda(this, name, method);
      return this;
    }


    public AddEnvironment(name: string, value: string): LAMBDA {
      this.Super.addEnvironment(name, value);
      return this;
    }
    
}

