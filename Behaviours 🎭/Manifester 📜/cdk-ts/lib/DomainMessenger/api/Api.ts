import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apiGW from 'aws-cdk-lib/aws-apigateway';
import * as sqs from 'aws-cdk-lib/aws-sqs';

export class API extends cdk.aws_apigateway.RestApi {

    Role: iam.Role;

    constructor(scope: Construct, id: string) {

        super(scope, id,{
            description: 'APIGW-SQS REST API Gateway',
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

        this.Role = new iam.Role(this, 'ReceiverApiRole', {
          assumedBy: new iam.ServicePrincipal('apigateway.amazonaws.com'),
        });

    }


    Arn(): string {
        //store the gateway ARN for use with our WAF stack
        //https://serverlessland.com/patterns/apigw-waf-cdk
        //https://github.com/cdk-patterns/serverless/blob/main/the-waf-apigateway/typescript/lib/api-gateway-stack.ts
        return `arn:aws:apigateway:${cdk.Stack.of(this).region}::/restapis/${this.restApiId}/stages/${this.deploymentStage.stageName}`
      
    }
    

    SendMessagesTo(queue: sqs.Queue) {
      
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
      this.root.addMethod('POST', sendMessageIntegration, {
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

    }

}