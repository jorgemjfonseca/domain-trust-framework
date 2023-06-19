import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apiGW from 'aws-cdk-lib/aws-apigateway';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import { WAF } from '../WAF/WAF';
import { WORKFLOW } from '../WORKFLOW/WORKFLOW';
import { LogGroup, RetentionDays } from "aws-cdk-lib/aws-logs";
import { LAMBDA } from '../LAMBDA/LAMBDA';
import { STACK } from '../STACK/STACK';

export class API  {

    Scope: STACK;
    Role: iam.Role;
    Super: cdk.aws_apigateway.RestApi;

    constructor (scope: STACK, api: cdk.aws_apigateway.RestApi)
    {
      this.Scope = scope;
      this.Super = api;

      this.Role = new iam.Role(scope, api.restApiName + 'Role', {
        assumedBy: new iam.ServicePrincipal('apigateway.amazonaws.com'),
      });
    }


    public static New(scope: STACK, id: string = 'Api'): API {
        const name = scope.stackName + id;

        const sup = new cdk.aws_apigateway.RestApi(scope, id,{
            restApiName: name,
            description: name,
            deployOptions: {
              stageName: 'dev',
              accessLogDestination: 
                new apiGW.LogGroupLogDestination(
                  new LogGroup(scope, id + "LogGroup", {
                    logGroupName: name,
                    retention: RetentionDays.ONE_DAY,
                    removalPolicy: cdk.RemovalPolicy.DESTROY
                  })
                )
            },
            // Enable CORS
            defaultCorsPreflightOptions: {
              allowHeaders: [
                'Content-Type',
                'X-Amz-Date',
                'Authorization',
                'X-Api-Key',
              ],
              allowMethods: ['OPTIONS', 'GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
              allowOrigins: ['*'],
            },
        });

        const ret = new API(scope, sup);

        return ret;
    }


    public Export(alias: string): API {
      new cdk.CfnOutput(this.Super, alias, {
        value: this.Super.restApiId,
        exportName: alias,
      });
      new cdk.CfnOutput(this.Super, alias + 'Root', {
        value: this.Super.restApiRootResourceId,
        exportName: alias,
      });
      return this;
    }


    public static Import(scope: STACK, alias: string): API {
      const apiId = cdk.Fn.importValue(alias);
      const rootResourceId = cdk.Fn.importValue(alias + 'Root');
      //const sup = cdk.aws_apigateway.RestApi.fromRestApiId(scope, alias, apiId);
      const sup = cdk.aws_apigateway.RestApi.fromRestApiAttributes(scope, alias, { 
          restApiId: apiId,
          rootResourceId: rootResourceId
      });
      const ret = new API(scope, sup as cdk.aws_apigateway.RestApi);
      return ret;
    }
    

    public Arn(): string {
        //store the gateway ARN for use with our WAF stack
        //https://serverlessland.com/patterns/apigw-waf-cdk
        //https://github.com/cdk-patterns/serverless/blob/main/the-waf-apigateway/typescript/lib/api-gateway-stack.ts
        return `arn:aws:apigateway:${cdk.Stack.of(this.Super).region}::/restapis/${this.Super.restApiId}/stages/${this.Super.deploymentStage.stageName}`
      
    }
    

    //https://gist.github.com/statik/f1ac9d6227d98d30c7a7cec0c83f4e64
    public AssociateWaf(waf: WAF): API {
      waf.AssociateApi(this);
      return this;  
    }


    public SendToQueue(queue: sqs.Queue, resource: cdk.aws_apigateway.Resource): API {
    
      queue.grantSendMessages(this.Role);

      // Api Gateway Direct Integration
      const sendMessageIntegration = new apiGW.AwsIntegration({
        service: 'sqs',
        path: `${process.env.CDK_DEFAULT_ACCOUNT}/${queue.queueName}`,
        integrationHttpMethod: 'POST',
        options: {
          credentialsRole: this.Role,
          requestParameters: {
            'integration.request.header.Content-Type': `'application/x-www-form-urlencoded'`,
          },
          requestTemplates: {
            'application/json': 'Action=SendMessage&MessageBody=$input.body',
          },
          integrationResponses: [
            {
              statusCode: '200',
            },
            {
              statusCode: '400',
            },
            {
              statusCode: '500',
            }
          ]
        },
      });
        
      // post method
      resource.addMethod('POST', sendMessageIntegration, {
        methodResponses: [
          {
            statusCode: '400',
          },
          { 
            statusCode: '200',
          },
          {
            statusCode: '500',
          }
        ]
      });

      return this;
    }


    public AddResource(resourceName: string): cdk.aws_apigateway.Resource {
      return this.Super.root.addResource(resourceName);
    }


    public GetResourceAtPath(path: string): cdk.aws_apigateway.Resource {
      return this.Super.root.resourceForPath(path);
    }


    public SendToWorkflow(wf: WORKFLOW, resource: cdk.aws_apigateway.Resource) {
      const credentialsRole = new iam.Role(this.Scope, "getRole", {
        assumedBy: new iam.ServicePrincipal("apigateway.amazonaws.com"),
      });
      
      credentialsRole.attachInlinePolicy(
        new iam.Policy(this.Scope, "getPolicy", {
          statements: [
            new iam.PolicyStatement({
              actions: ["states:StartExecution"],
              effect: iam.Effect.ALLOW,
              resources: [wf.Super.stateMachineArn],
            }),
          ],
        })
      );
      
      resource.addMethod(
        "GET",
        new apiGW.AwsIntegration({
          service: "states",
          action: "StartExecution",
          integrationHttpMethod: "POST",
          options: {
            credentialsRole,
            integrationResponses: [
              {
                statusCode: "200",
                responseTemplates: {
                  "application/json": `{"done": true}`,
                },
              },
            ],
            requestTemplates: {
              "application/json": `{
                    "input": "{\\"prefix\\":\\"prod\\"}",
                    "stateMachineArn": "${wf.Super.stateMachineArn}"
                  }`,
            },
          },
        }),
        {
          methodResponses: [{ statusCode: "200" }],
        }
      );
    }


    SendToLambda(lambda: LAMBDA, name: string, method: string = "POST") {
      const resource = 
        this.GetResourceAtPath("/" + name.toLowerCase()) ??
        this.AddResource(name);
      
      resource.addMethod(method, 
        new apiGW.LambdaIntegration(lambda.Super));
    }


}