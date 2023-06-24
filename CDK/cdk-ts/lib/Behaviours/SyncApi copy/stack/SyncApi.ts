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

declare module '../../../Common/LAMBDA/LAMBDA' {
  interface LAMBDA {
    HandlesSyncApi(action: string): LAMBDA;
  }
}

//https://quip.com/RnO6Ad0BuBSx/-Sync-API
export class SyncApi extends STACK {

  private static readonly MAP = 'SyncApiMap';
  private static readonly MAPPER = 'SyncApiMapper';
  
  public static readonly API = 'SyncApi';
  public static readonly SENDER = 'SyncApiSenderFn';
  public static readonly RECEIVER = 'SyncApiReceiverFn';

  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, SyncApi.name, props);

    
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
  
    const waf = WAF
      .New(this, 'WAFv2');

    const certificate = CERTIFICATE
      .Import(this, DomainDns.CERTIFICATE);

    const dns = ROUTE53
      .Import(this, DomainDns.HOSTED_ZONE);

    // API GATEWAY
    const api = API.New(this)
      .AssociateWaf(waf)
      .AddCertificate("dtfw."+domainName, certificate)
      .AddToRoute53("dtfw", dns)
      .Export(SyncApi.API);

    // ROUTER MAP
    const map = DYNAMO
      .New(this, 'Map')
      .Export(SyncApi.MAP);

    // RECEIVER FUNCTION
    LAMBDA
      .New(this, "ReceiverFn")
      .ReadsFromDynamoDB(map)
      .GrantLambdaInvocation()
      .SetApiRoot(api)
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
