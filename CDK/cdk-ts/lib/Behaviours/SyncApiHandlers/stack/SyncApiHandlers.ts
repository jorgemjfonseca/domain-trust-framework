import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { SyncApiEndpoint } from '../../SyncApiEndpoint/stack/SyncApiEndpoint';
import { SyncApiDkim } from '../../SyncApiDkim/stack/SyncApiDkim';
import { DomainName } from '../../DomainName/stack/DomainName';
import { CUSTOM } from '../../../Common/CUSTOM/CUSTOM';

export interface SyncApiHandlersDependencies {
  syncApiDkim: SyncApiDkim
}

// 👉 https://quip.com/RnO6Ad0BuBSx/-Sync-API
export class SyncApiHandlers extends STACK {

  private static readonly MAP = 'SyncApiMap';
  private static readonly MAPPER = 'SyncApiMapper';

  private static readonly SENDER = 'SyncApiSenderFn';
  private static readonly RECEIVER = 'SyncApiReceiverFn';

  public static GetSenderFn(scope: STACK) {
    return LAMBDA.Import(scope, this.SENDER);
  }

  public static GetReceiverFn(scope: STACK) {
    return LAMBDA.Import(scope, this.RECEIVER);
  }

  public static New(scope: Construct, deps: SyncApiHandlersDependencies): SyncApiHandlers {
    const ret = new SyncApiHandlers(scope);
    ret.addDependency(deps.syncApiDkim);
    return ret;
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, SyncApiHandlers.name, {
      description: 'Creates handlers for Sender and Receiver Map.',
      ...props
    });

    // DEPENDENCIES
    const domainName = DomainName.GetDomainName(this);

    // BLOCKS
    this.SetUpSender(domainName);
    this.SetUpReceiver(domainName);
  }



  private SetUpSender(domainName: string) {
      
    const signer = LAMBDA
      .Import(this, SyncApiDkim.SIGNER_FN);

    const senderFn = LAMBDA
        .New(this, "SenderFn")
        .GrantLambdaInvocation()
        .GrantSecretsManagerReadWrite()
        .Export(SyncApiHandlers.SENDER)
        .AddEnvironment('SIGNER_FN', signer.FunctionName())
        .AddEnvironment('DOMAIN_NAME', domainName);
  }


  private SetUpReceiver(domainName: string) {

    // ROUTER MAP
    const map = DYNAMO
      .New(this, 'Map')
      .Export(SyncApiHandlers.MAP);

    const dkimReaderFn = LAMBDA
      .Import(this, SyncApiDkim.DKIM_READER_FN);

    const validatorFn = LAMBDA
      .Import(this, SyncApiDkim.VALIDATOR_FN);

    // RECEIVER FUNCTION
    LAMBDA
      .New(this, "ReceiverFn")
      .ReadsFromDynamoDB(map)
      .GrantLambdaInvocation()
      .AddEnvironment('DKIM_READER_FN', dkimReaderFn.FunctionName())
      .AddEnvironment('VALIDATOR_FN', validatorFn.FunctionName())
      .AddEnvironment('DOMAIN_NAME', domainName)
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
