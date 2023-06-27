import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { API } from '../../../Common/API/API';
import { SyncApiEndpoint } from '../../SyncApiEndpoint/stack/SyncApiEndpoint';
import { SyncApiDkim } from '../../SyncApiDkim/stack/SyncApiDkim';
import { DomainName } from '../../DomainName/stack/DomainName';



// 👉 https://quip.com/RnO6Ad0BuBSx/-Sync-API
export class SyncApiHandlers extends STACK {

  private static readonly MAP = 'SyncApiMap';
  private static readonly MAPPER = 'SyncApiMapper';

  public static readonly SENDER = 'SyncApiSenderFn';
  public static readonly RECEIVER = 'SyncApiReceiverFn';

  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, SyncApiHandlers.name, props);

    // DEPENDENCIES
    const api = API.Import(this, SyncApiEndpoint.API);
    const domainName = DomainName.GetDomainName(this);

    // BLOCKS
    this.SetUpSender(domainName);
    this.SetUpReceiver(domainName, api);
    
  }


  private SetUpSender(domainName: string) {
      
    // SENDER FUNCTION 
    const senderFn = LAMBDA
        .New(this, "SenderFn")
        .GrantLambdaInvocation()
        .Export(SyncApiHandlers.SENDER)
        .AddEnvironment('SIGNER_FN', SyncApiDkim.SIGNER_FN)
        .AddEnvironment('DOMAIN_NAME', domainName);
  }


  private SetUpReceiver(domainName: string, api: API) {

    // ROUTER MAP
    const map = DYNAMO
      .New(this, 'Map')
      .Export(SyncApiHandlers.MAP);

    // RECEIVER FUNCTION
    LAMBDA
      .New(this, "ReceiverFn")
      .ReadsFromDynamoDB(map)
      .GrantLambdaInvocation()
      .AddEnvironment('DKIM_READER_FN', SyncApiDkim.DKIM_READER_FN)
      .AddEnvironment('VALIDATOR_FN', SyncApiDkim.VALIDATOR_FN)
      .AddEnvironment('DOMAIN_NAME', domainName)
      .AddApiMethod(api, 'inbox', 'POST')
      .Export(SyncApiHandlers.RECEIVER);

    // REGISTER EXTENSION
    LAMBDA.prototype.HandlesSyncApi = function(action: string) {
      SyncApiHandlers.HandlesSyncApi(this.Scope, action, this);
      return this;
    };

  }
  

  public static HandlesSyncApi(scope: STACK, action: string, lambda: LAMBDA) 
  {
    const map = DYNAMO
      .Import(scope, SyncApiHandlers.MAP);
      
    map.PutItem({
      'ID': {'S':action},
      'Target': {'S':lambda.Super.functionName}
    });
  }

}


declare module '../../../Common/LAMBDA/LAMBDA' {
  interface LAMBDA {
    HandlesSyncApi(action: string): LAMBDA;
  }
}
