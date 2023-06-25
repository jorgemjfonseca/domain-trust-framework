import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { API } from '../../../Common/API/API';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { STACK } from '../../../Common/STACK/STACK';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { WAF } from '../../../Common/WAF/WAF';
import { KMS_KEY } from '../../../Common/KEY/KMS_KEY';
import { DomainDns } from '../../DomainDns/stack/DomainDns';
import { CERTIFICATE } from '../../../Common/CERTIFICATE/CERTIFICATE';
import { ROUTE53 } from '../../../Common/ROUTE53/ROUTE53';
import { CUSTOM } from '../../../Common/CUSTOM/CUSTOM';
import { PYTHON } from '../../../Common/PYTHON/PYTHON';

declare module '../../../Common/LAMBDA/LAMBDA' {
  interface LAMBDA {
    HandlesSyncApi(action: string): LAMBDA;
  }
}



// 👉 https://quip.com/RnO6Ad0BuBSx/-Sync-API
export class SyncApi extends STACK {

  private static readonly MAP = 'SyncApiMap';
  private static readonly MAPPER = 'SyncApiMapper';
  
  public static readonly API = 'SyncApi';
  public static readonly SENDER = 'SyncApiSenderFn';
  public static readonly RECEIVER = 'SyncApiReceiverFn';

  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, SyncApi.name, props);

    // SENDING
    this.SetUpSender();

    // RECEIVING
    const api = this.SetUpApi()
    this.SetUpCustomDomain(api);
    this.SetUpFirewall(api)
    this.SetUpReceiver(api);

  }



  private SetUpSender() {

    const domainName = this
      .Import(DomainDns.DOMAIN_NAME);

    const key = KMS_KEY
      .Import(this, DomainDns.KEY);
      
    // SENDER FUNCTION 
    const senderFn = LAMBDA
        .New(this, "SenderFn")
        .AddEnvironment('DOMAIN_NAME', domainName)
        .SignsWithKmsKey(key)
        .Export(SyncApi.SENDER);
  }


  private SetUpApi(): API {
    const api = API
      .New(this)
      .Export(SyncApi.API);

    return api;
  }


  private SetUpFirewall(api: API) {
    const waf = WAF
      .New(this, 'WAFv2')
      .AssociateApi(api);
  }



  private SetUpCustomDomain(api: API) {

    const rootDomain = 
      //'105b4478-eaa5-4b73-b2a5-4da2c3c2dac0.dev.dtfw.org';
      this.Import(DomainDns.DOMAIN_NAME);
    
    const dns = ROUTE53
      //.ImportFromDomainName(this, rootDomain);
      .ImportFromAlias(this, DomainDns.HOSTED_ZONE)  

    const certificate = CERTIFICATE
      .Import(this, DomainDns.CERTIFICATE);
  

    // CAN'T SET APIGW IN ROUTE53 USING CDK WITH MULTIPLE STACKS, 
    //   SO SWITCHIN TO A CUSTOM CDK STEP INSTEAD.
    const domainName = api.AddCertificate('dtfw', rootDomain, certificate)
    this.Export('ApiAliasHostedZoneId', domainName.domainNameAliasHostedZoneId);
    this.Export('ApiAliasDomainName', domainName.domainNameAliasDomainName);
    this.Export('ApiDomainName', domainName.domainName);
    this.Export('ApiEndpoint', api.DefaultDomain())

    const setAliasFn = LAMBDA
      .New(this, 'SetAliasFn', {
        runtime: LAMBDA.PYTHON_3_10,
        handler: 'index.on_event'
      })
      .GrantRoute53FullAccess();
    
    CUSTOM
      .New('Custom', setAliasFn, {
        //apiEndpoint: api.DefaultDomain(), 
        apiDomain: domainName.domainName,
        apiHostedZoneId: domainName.domainNameAliasHostedZoneId,
        apiAlias: domainName.domainNameAliasDomainName,
        customDomain: 'dtfw.'+rootDomain,
        hostedZoneId: dns.Super.hostedZoneId,
      });
      
    // Test 👉 https://www.sslshopper.com/ssl-checker.html
    // Test 👉 https://www.digicert.com/help/
  }


  private SetUpReceiver(api: API) {

    const getPublicKeyFn = PYTHON
      .New(this, 'GetPublicKeyFn')
      .FunctionName();

    const validateSignatureFn = PYTHON
      .New(this, 'ValidateSignatureFn')
      .FunctionName();

    // ROUTER MAP
    const map = DYNAMO
      .New(this, 'Map')
      .Export(SyncApi.MAP);

    // RECEIVER FUNCTION
    LAMBDA
      .New(this, "ReceiverFn")
      .ReadsFromDynamoDB(map)
      .GrantLambdaInvocation()
      .AddApiMethod(api, 'inbox', 'POST')
      //.SetApiRoot(api)
      .AddEnvironment('GET_PUBLIC_KEY_FN', getPublicKeyFn)
      .AddEnvironment('VALIDATE_SIGNATURE_FN', validateSignatureFn)
      .Export(SyncApi.RECEIVER);

    // REGISTER EXTENSION
    LAMBDA.prototype.HandlesSyncApi = function(action: string) {
      SyncApi.HandlesSyncApi(this.Scope, action, this);
      return this;
    };

  }


  public static HandlesSyncApi(scope: STACK, action: string, lambda: LAMBDA) 
  {
    const map = DYNAMO
      .Import(scope, SyncApi.MAP);
      
    map.PutItem({
      'ID': {'S':action},
      'Target': {'S':lambda.Super.functionName}
    });
  }


}
