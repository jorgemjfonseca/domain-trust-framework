import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apiGW from 'aws-cdk-lib/aws-apigateway';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import { WAF } from '../Waf/Waf';

export class API  {

    Scope: cdk.Stack;
    Role: iam.Role;
    Super: cdk.aws_apigateway.RestApi;

    constructor (scope: cdk.Stack, api: cdk.aws_apigateway.RestApi)
    {
      this.Scope = scope;
      this.Super = api;

      this.Role = new iam.Role(scope, 'ReceiverApiRole', {
        assumedBy: new iam.ServicePrincipal('apigateway.amazonaws.com'),
      });
    }


    public static New(scope: cdk.Stack, id: string = 'Api'): API {
        
        const sup = new cdk.aws_apigateway.RestApi(scope, id,{
          restApiName: scope.stackName + id,
            description: scope.stackName + id,
            deployOptions: {
              stageName: 'dev',
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
      return this;
    }


    public static Import(scope: cdk.Stack, alias: string): API {
      const apiId = cdk.Fn.importValue(alias);
      const sup = cdk.aws_apigateway.RestApi.fromRestApiId(scope, alias, apiId);
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
    AssociateWaf(waf: WAF): API {
      waf.AssociateApi(this);
      return this;  
    }


    public SendMessagesTo(queue: sqs.Queue): API {
    
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
      this.Super.root.addMethod('POST', sendMessageIntegration, {
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

}