import * as cdk from 'aws-cdk-lib';
import * as acm from 'aws-cdk-lib/aws-certificatemanager';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apiGW from 'aws-cdk-lib/aws-apigateway';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as route53 from 'aws-cdk-lib/aws-route53';
import { WAF } from '../WAF/WAF';
import { WORKFLOW } from '../WORKFLOW/WORKFLOW';
import { LogGroup, RetentionDays } from "aws-cdk-lib/aws-logs";
import { LAMBDA } from '../LAMBDA/LAMBDA';
import { STACK } from '../STACK/STACK';
import { CONSTRUCT } from '../CONSTRUCT/CONSTRUCT';
import { CERTIFICATE } from '../CERTIFICATE/CERTIFICATE';
import { ROUTE53 } from '../ROUTE53/ROUTE53';
import { ARecord, RecordTarget } from 'aws-cdk-lib/aws-route53';
import * as targets from 'aws-cdk-lib/aws-route53-targets';

export interface API_CustomDomain {
  certificate: CERTIFICATE;
  zone: ROUTE53;
  rootDomain: string,
  domainPrefix?: string
}

export interface API_Options {
  id?: string;
  customDomain?: API_CustomDomain
}

export class API extends CONSTRUCT {

    Role: iam.Role;
    Super: cdk.aws_apigateway.RestApi;
    

    constructor (scope: STACK, api: cdk.aws_apigateway.RestApi)
    {
      super(scope);
      this.Super = api;

      this.Role = new iam.Role(scope, api.restApiName + 'Role', {
        assumedBy: new iam.ServicePrincipal('apigateway.amazonaws.com'),
      });
    }


    public static New(scope: STACK, props?: API_Options): API {
        const id =  props?.id ?? 'Api';
        const name = `${scope.Name}-${id}`;

        const cd = props?.customDomain;
      
        // e.g., 'apiUrl2.105b4478-eaa5-4b73-b2a5-4da2c3c2dac0.dev.dtfw.org'
        const fullDomainName = 
          cd?.domainPrefix + 
          (cd?.domainPrefix?'.':'') +
          cd?.rootDomain

        // ENABLE CUSTOM DOMAINS
        // 👉 https://us-west-2.console.aws.amazon.com/apigateway/main/publish/domain-names?region=us-west-2
        const domainOptions = cd?.certificate && cd.rootDomain ?
          {
            domainName: fullDomainName,
            certificate: cd.certificate.Super,
            // EDGE requires the certificate to be in eu-west-1
            endpointType: cdk.aws_apigateway.EndpointType.REGIONAL,
          }
          : undefined;

        // ENABLE CORS
        // 👉 https://us-west-2.console.aws.amazon.com/apigateway/home?region=us-west-2#/apis/76vhnh0x3j/resources/bff2uyep4j/enable-cors
        const corsOption = {
          allowHeaders: [
            'Content-Type',
            'X-Amz-Date',
            'Authorization',
            'X-Api-Key',
          ],
          allowMethods: ['OPTIONS', 'GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
          allowOrigins: ['*'],
        }

        // SETUP DEPLOYMENT
        // 👉 https://us-west-2.console.aws.amazon.com/apigateway/home?region=us-west-2#/apis/76vhnh0x3j/stages/dev
        const deployOptions = {
          stageName: 'dev',
          accessLogDestination: 
            new apiGW.LogGroupLogDestination(
              new LogGroup(scope, id + "LogGroup", {
                logGroupName: name,
                retention: RetentionDays.ONE_DAY,
                removalPolicy: cdk.RemovalPolicy.DESTROY
              })
            )
        };

        // CREATE THE API
        // 👉 https://us-west-2.console.aws.amazon.com/apigateway/main/apis?region=us-west-2
        const api = new cdk.aws_apigateway.RestApi(scope, id,{
            deploy: true,
            retainDeployments: false,
            restApiName: name,
            description: name,
            cloudWatchRole: true,
            // EDGE requires the certificate to be in eu-west-1
            endpointTypes: [ cdk.aws_apigateway.EndpointType.REGIONAL ],
            defaultCorsPreflightOptions: corsOption,
            deployOptions: deployOptions,
            domainName: domainOptions,
        });

        // ADD DNS RECORD FOR CUSTOM DOMAIN
        // 👉 https://us-east-1.console.aws.amazon.com/route53/v2/hostedzones?region=us-east-1#ListRecordSets/Z09251313MWYO7KRJUSHG
        // 👉 https://stackoverflow.com/questions/63220019/cdk-api-gateway-route53-lambda-custom-domain-name-not-working
        if (cd?.zone) {
            const target = RecordTarget
              .fromAlias(new targets.ApiGateway(api));

            new ARecord(scope, scope.RandomName('ApiRecordA'), {
              zone: cd.zone.Super,
              // e.g., 'apiUrl2.105b4478-eaa5-4b73-b2a5-4da2c3c2dac0.dev.dtfw.org'
              recordName: fullDomainName,
              target: target,
              ttl: cdk.Duration.minutes(1),
            });
        }
        
        const ret = new API(scope, api);

        return ret;
    }


    /**
     * @deprecated 
     *    Don't use for a CNAME on ROUTE53, it will return the wrong certificate.
     *    Instead, use [IDomainName.domainNameAliasHostedZoneId].
     *    Details: https://repost.aws/knowledge-center/api-gateway-domain-certificate
     */
    public DefaultDomain(): string {
      const url = this.Super.url;
      const stageName = this.Super.deploymentStage.stageName;
      const domainName = url
        .replace(stageName, '')
        .replace(/^https?:\/\//, '')
        .replace('//', '')
        .replace('/', '')
        .replace('/', '');
      return domainName;
    }


    public AddCertificate(
      domainPrefix: string, 
      rootDomain: string, 
      certificate: CERTIFICATE
    ): apiGW.DomainName {
      
      // e.g., 'apiUrl2.105b4478-eaa5-4b73-b2a5-4da2c3c2dac0.dev.dtfw.org'
      const fullDomainName = 
        domainPrefix + 
        (domainPrefix?'.':'') +
        rootDomain;

      const domainName = this.Super.addDomainName('DomainName', {
        domainName: fullDomainName,
        certificate: certificate.Super
      });

      return domainName;
    }


    public Export(alias: string): API {
      new cdk.CfnOutput(this.Super, alias, {
        value: this.Super.restApiId,
        exportName: alias,
      });
      new cdk.CfnOutput(this.Super, alias + 'Root', {
        value: this.Super.restApiRootResourceId,
        exportName: alias + 'Root',
      });
      return this;
    }


    /** 
    * @deprecated: Not tested properly!
    */
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
        // 👉 https://serverlessland.com/patterns/apigw-waf-cdk
        // 👉 https://github.com/cdk-patterns/serverless/blob/main/the-waf-apigateway/typescript/lib/api-gateway-stack.ts
        return `arn:aws:apigateway:${cdk.Stack.of(this.Super).region}::/restapis/${this.Super.restApiId}/stages/${this.Super.deploymentStage.stageName}`
      
    }
    

    // 👉 https://gist.github.com/statik/f1ac9d6227d98d30c7a7cec0c83f4e64
    public AssociateWaf(waf: WAF): API {
      waf.AssociateApi(this);
      return this;  
    }


    /**
     * @deprecated 'Not tested properly, use a SendToLambda() instead.'
     */
    public SendToQueue(queue: sqs.Queue, resource: cdk.aws_apigateway.Resource): API {
      throw Error('Not tested properly, use a SendToLambda() instead.');

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
            { statusCode: '200' },
            { statusCode: '400' },
            { statusCode: '500' }
          ]
        },
      });
        
      // post method
      resource.addMethod('POST', sendMessageIntegration, {
        methodResponses: [
          { statusCode: '200' },
            { statusCode: '400' },
            { statusCode: '500' }
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

    
    /**
     * @deprecated 'Not tested properly, use a SendToLambda() instead.'
     */
    public SendToWorkflow(wf: WORKFLOW, resource: cdk.aws_apigateway.Resource) {
      throw Error('Not tested properly, use a SendToLambda() instead.');

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


    private SetAutoScaling(fn: LAMBDA, name: string): lambda.Alias {

      const liveAlias = new lambda.Alias(this, fn.Name+'Alias', {
        aliasName: 'live',
        version: fn.Super.currentVersion,
      })

      const target = liveAlias.addAutoScaling({
        minCapacity: 1,
        maxCapacity: 100
      })

      target.scaleOnUtilization({
        utilizationTarget: 0.75,
      })

      return liveAlias;
    }


    SendToLambda(fn: LAMBDA, name: string, method: string = "POST"): LAMBDA {

      const resource = 
        this.GetResourceAtPath("/" + name?.toLowerCase()) ??
        this.AddResource(name);

      const liveAlias = this.SetAutoScaling(fn, name);

      resource.addMethod(method, 
        new apiGW.LambdaIntegration(liveAlias, {
          proxy: true,
          integrationResponses: [
            { statusCode: '200' },
            { statusCode: '400' },
            { statusCode: '500' }
          ]
        }), {
          methodResponses: [
            { statusCode: '200' },
            { statusCode: '400' },
            { statusCode: '500' }
          ]
        });

      // Grant permission to execute
      // 👉 https://stackoverflow.com/questions/62201988/aws-cdk-how-to-grant-invoke-permissions-on-a-lambda-to-api-gateway-before-depl
      fn.Super.addPermission('PermitAPIGInvocation', {
        principal: new iam.ServicePrincipal('apigateway.amazonaws.com'),
        //sourceArn: this.Super.arnForExecuteApi('*')
      });

      // 👉 https://stackoverflow.com/questions/55900479/cross-stack-lambda-and-api-gateway-permissions-with-aws-cdk
      fn.Super.grantInvoke(
        new iam.ServicePrincipal('apigateway.amazonaws.com'));

      return fn;
    }


    SetRootToLambda(lambda: LAMBDA, method: string = "POST"): LAMBDA {
      this.Super.root.addMethod(method, 
        new apiGW.LambdaIntegration(lambda.Super));
        return lambda;
    }


}