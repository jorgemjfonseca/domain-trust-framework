import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as events from 'aws-cdk-lib/aws-events';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as s3n from 'aws-cdk-lib/aws-s3-notifications'
import * as sources from "aws-cdk-lib/aws-lambda-event-sources";
import * as targets from 'aws-cdk-lib/aws-events-targets';
import { KMS_KEY } from '../KEY/KMS_KEY';
import { BUS } from '../BUS/BUS';
import { DLQ, SQS } from '../SQS/SQS';
import { S3 } from '../S3/S3';
import { WORKFLOW } from '../WORKFLOW/WORKFLOW';
import { API } from '../API/API';
import { DYNAMO } from '../DYNAMO/DYNAMO';
import { NEPTUNE } from '../NEPTUNE/NEPTUNE';
import * as path from 'path';
import { STACK } from '../STACK/STACK';
import { CONSTRUCT } from '../CONSTRUCT/CONSTRUCT';
import { EC2_KEY } from '../KEY/EC2_KEY';
import { APPCONFIG } from '../APPCONFIG/APPCONFIG';


export interface LAMBDAparams {
  runtime?: lambda.Runtime;
  handler?: string;
  super?: cdk.aws_lambda.FunctionProps;
  description?: string;
}



export class LAMBDA extends CONSTRUCT {

    Name: string;
    Role: iam.Role;
    Super: lambda.Function;

    static PYTHON_3_10 = lambda.Runtime.PYTHON_3_10;

    constructor(scope: STACK, sup: lambda.Function)
    {
        super(scope);
        this.Super = sup;
        this.Name = sup.functionName;
        this.Role = sup.role as iam.Role
    }

    public static New(
      scope: STACK, 
      id: string, 
      props?: LAMBDAparams
    ): LAMBDA {

        //const dlq = DLQ.New(scope, id + "-Dlq");
      
        const role = new iam.Role(scope, id+'Role', {
          assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com')
        });

        role.addManagedPolicy(
          iam.ManagedPolicy.fromManagedPolicyArn(scope, 
            scope.Name + id + "BasicExecutionRole", 
            'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'));

        const sup = new lambda.Function(scope, id, {
          role: role,

          functionName: `${scope.Name}-${id}`,
          description: props?.description,
          //deadLetterQueue: dlq.Super,
          memorySize: 1024, 
          timeout: cdk.Duration.seconds(30),

          ...props?.super,

          runtime: 
            props?.runtime
            ?? props?.super?.runtime 
            ?? lambda.Runtime.PYTHON_3_10,
          code: 
            props?.super?.code 
            ?? lambda.Code.fromAsset(path.join(this.CallerDirname(), '../lambda/' + id)),
          handler: 
            props?.handler 
            ?? props?.super?.handler 
            ?? 'index.handler',
        });

        const fn = new LAMBDA(scope, sup);

        //dlq.Super.grantSendMessages(fn.Super);

        return fn;
    }

    public static CallerDirname({ depth = 1 } = {}): string {
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

    
    /**
     * @deprecated
     */
    private static FromFunctionName(scope: STACK, name: string) {
      return lambda.Function
        .fromFunctionName(scope, name, name);
    }
    

    // Exports to a parameter.
    public Export(alias: string): LAMBDA {
      new cdk.CfnOutput(this.Super, alias, {
        value: this.Super.functionName,
        exportName: alias,
      });
      new cdk.CfnOutput(this.Super, alias+'Arn', {
        value: this.Super.functionArn,
        exportName: alias + 'Arn',
      });
      new cdk.CfnOutput(this.Super, alias+'RoleArn', {
        value: this.Super.role?.roleArn + '',
        exportName: alias + 'RoleArn',
      });
      return this;
    }


    private static NewFromFunctionName(scope: STACK, name: string): LAMBDA {
      const sup = lambda.Function.fromFunctionName(scope, scope.RandomName(name), name);
      const ret = new LAMBDA(scope, sup as lambda.Function);
      return ret;
    }

    private static NewFromAttributes(scope: STACK, functionArn: string, roleArn: string): LAMBDA {
      const sup = lambda.Function.fromFunctionAttributes(
        scope, 
        scope.RandomName('fn'), {
          functionArn: functionArn,
          role: iam.Role.fromRoleArn(
            scope, 
            scope.RandomName('role'), 
            roleArn),
          sameEnvironment: true,
        });
      const ret = new LAMBDA(scope, sup as lambda.Function);
      return ret;
    }

    // Imports from a parameter.
    public static Import(scope: STACK, alias: string): LAMBDA {
      //const name = cdk.Fn.importValue(alias);
      //return LAMBDA.NewFromFunctionName(scope, name);
      const functionArn =  cdk.Fn.importValue(alias + 'Arn');
      const roleArn =  cdk.Fn.importValue(alias + 'RoleArn');
      return LAMBDA.NewFromAttributes(scope, functionArn, roleArn);
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
        ArnLike: { 'aws:SourceArn': bucket.Super.bucketArn, },
        StringEquals: { 'aws:SourceAccount': cdk.Aws.ACCOUNT_ID, }
      }));

      var destination = new s3n.LambdaDestination(this.Super);
      var prefix = 'DomainManifest.yaml'; 
      bucket.Super.addEventNotification(s3.EventType.OBJECT_CREATED, destination, { prefix: prefix });
      bucket.Super.addEventNotification(s3.EventType.OBJECT_REMOVED, destination, { prefix: prefix });

      return this;
    }


    public TriggeredBySQS(queue: SQS): LAMBDA {
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
      //source: string,
      detailType: string,
      props?: targets.LambdaFunctionProps): LAMBDA 
    {
      this.TriggeredByBus(eventBus, detailType, props);
      this.PublishesToBus(eventBus);
      return this;
    }


    public TriggeredByBus(
      eventBus: BUS,
      // e.g. { source: ["DTFW"], detailType: ["CREATE", "UPDATE", "DELETE"] }
      //source: string,
      detailType: string,
      props?: targets.LambdaFunctionProps): LAMBDA 
    {
      const name = this.Name + '-' + eventBus.Name;
      
      const eventRule = new events.Rule(this.Scope, detailType+'-Rule', {
        ruleName: name+'-Rule',
        eventBus: eventBus.Super,
        eventPattern: {
          //source: [ source ],
          detailType: [ detailType ]
        }
      });

      const dlq = DLQ.New(this.Scope, detailType+'-ByBus');

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

    public SignsWithKmsKey(key: KMS_KEY): LAMBDA {
      
      this.Super.addEnvironment("KEY_ARN", key.Super.keyArn);
      key.Super.grantEncrypt(this.Super);

      // 👉 https://github.com/aws/aws-cdk/issues/19914
      // 👉 https://docs.aws.amazon.com/kms/latest/developerguide/alias-authorization.html#alias-auth-resource-aliases
      this.Super.role?.addToPrincipalPolicy(
        new iam.PolicyStatement({
          actions: [
            "kms:Sign",
          ],
          resources: ['*'],

          // FILTER BY ALIAS IS NOT WORKING - IT BLOCKS.
          /* conditions: {
            StringEquals: {
              "kms:RequestAlias": key.Alias,
            },
          }, */

        }),
      )

      return this;
    }

    public SignsWithEc2Key(key: EC2_KEY): LAMBDA {
      key.Super.grantReadOnPrivateKey(this.Super);
      this.Super.addEnvironment("KEY_ARN", key.Super.keyPairName);
      return this;
    }

    public ReadsFromS3(s3: S3): LAMBDA {
      s3.Super.grantRead(this.Super);
      this.Super.addEnvironment("S3_NAME", s3.Super.bucketName);
      return this;
    }

    public WritesToS3(s3: S3): LAMBDA {
      s3.Super.grantReadWrite(this.Super);
      s3.Super.grantDelete(this.Super);
      s3.Super.grantPut(this.Super);
      this.Super.addEnvironment("S3_NAME", s3.Super.bucketName);
      return this;
    }


    public GrantKeyManagementServicePowerUser(): LAMBDA {
      return this.AttachManagedPolicy('AWSKeyManagementServicePowerUser');
    }

    public GrantCloudFormationReadOnlyAccess(): LAMBDA {
      return this.AttachManagedPolicy('AWSCloudFormationReadOnlyAccess');
    }

    public GrantAmazonAPIGatewayAdministrator(): LAMBDA {
      return this.AttachManagedPolicy('AmazonAPIGatewayAdministrator');
    }

    public GrantRoute53FullAccess(): LAMBDA {
      return this.AttachManagedPolicy('AmazonRoute53FullAccess');
    }
    
    public GrantSsmFullAccess(): LAMBDA {
      return this.AttachManagedPolicy('AmazonSSMFullAccess');
    }

    public GrantSecretsManagerReadWrite(): LAMBDA {
      return this.AttachManagedPolicy('SecretsManagerReadWrite');
    }

    /**
     * @deprecated Don't be lazy!
     */
    private GrantLambdaInvocation(): LAMBDA {
      return this.AttachManagedPolicy('AWSLambdaInvocation-DynamoDB');
    }

    public GrantConfigUserAccess(): LAMBDA {
      return this.AttachManagedPolicy('AWSConfigUserAccess');
    }

    public ReadsAppConfig(appConfig: APPCONFIG): LAMBDA {
      appConfig.AddEnvironment(this);
      this.GrantConfigUserAccess();
      
      this.Super.role?.attachInlinePolicy(
        new iam.Policy(this.Scope, "PolicyConfig", {
          statements: [
            new iam.PolicyStatement({
              actions: [
                "appconfig:StartConfigurationSession",
                "appconfig:GetLatestConfiguration"
              ],
              effect: iam.Effect.ALLOW,
              resources: ['*'],
            }),
          ],
        }));

      return this;
    }
    

    // https://bobbyhadz.com/blog/aws-cdk-iam-policy-example
    public AttachManagedPolicy(name: string): LAMBDA {
      // 👇 Use an AWS-Managed Policy
      const managedPolicy = iam.ManagedPolicy.fromAwsManagedPolicyName(name);

      // 👇 attach the Managed Policy to the Role
      this.Super.role?.addManagedPolicy(managedPolicy);
      return this;
    }

    
    public InvokesLambda(fn: LAMBDA, envName?: string): LAMBDA {
      // Error: "Cannot get policy fragment of PublisherBehaviour/${Token[TOKEN.1378]}, resource imported without a role"
      // But it's already authorized for any Lambda invocation, so we're good.
      fn.Super.grantInvoke(this.Super);
      if (envName)
        this.Super?.addEnvironment(envName, fn.FunctionName());
      return this;
    }

    
    private getTableParam(alias?: string): string {
      const name = "TABLE" + (alias ? "_" + alias.toUpperCase() : "");
      if (name == 'TABLE_UNDEFINED')
        throw new Error('LAMBDA.ENV[table] cannot be TABLE_UNDEFINED.');
      return name;
    }

    public WritesToDynamoDB(dynamo: DYNAMO, alias: string): LAMBDA {
      dynamo.Super.grantReadWriteData(this.Super);
      this.Super.addEnvironment(alias, dynamo.Super.tableName);
      return this;
    }

    public ReadsFromDynamoDB(dynamo: DYNAMO, alias: string): LAMBDA {
      dynamo.Super.grantReadData(this.Super);
      this.Super.addEnvironment(alias, dynamo.Super.tableName);
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


    public AddApiMethod(api: API, name: string, methods: string[] = ["POST"]): LAMBDA {
      return api.SendToLambda(this, name, methods);
    }

    public SetApiRoot(api: API, method: string = "POST"): LAMBDA {
      return api.SetRootToLambda(this, method);
    }


    public AddEnvironment(name: string, value: string): LAMBDA {
      this.Super.addEnvironment(name, value);
      return this;
    }

    public FunctionName(): string {
      return this.Super.functionName;
    }

    
}

