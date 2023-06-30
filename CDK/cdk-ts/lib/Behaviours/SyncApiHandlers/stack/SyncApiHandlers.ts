import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { SyncApiDkim } from '../../SyncApiDkim/stack/SyncApiDkim';
import { DomainName } from '../../DomainName/stack/DomainName';

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
      
    const signer = SyncApiDkim.GetSigner(this);

    const senderFn = LAMBDA
        .New(this, "SenderFn")
        .InvokesLambda(signer, 'SIGNER_FN')
        .GrantSecretsManagerReadWrite()
        .Export(SyncApiHandlers.SENDER)
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
      .InvokesLambda(dkimReaderFn, 'DKIM_READER_FN')
      .InvokesLambda(validatorFn, 'VALIDATOR_FN')
      .AddEnvironment('DOMAIN_NAME', domainName)
      .Export(SyncApiHandlers.RECEIVER);

    // REGISTER EXTENSION
    LAMBDA.prototype.HandlesSyncApi = function(action: string) {
      SyncApiHandlers.HandlesSyncApi(this.Scope, action, this);
      return this;
    };

  }
  

  public static HandlesSyncApi(scope: STACK, action: string, fn: LAMBDA) 
  {
    const map = DYNAMO
      .Import(scope, SyncApiHandlers.MAP);
      
    // Register the function name.
    map.PutItem({
      'ID': {'S':action},
      'Target': {'S':fn.FunctionName()}
    });

    // Add invoke permission.
    SyncApiHandlers
      .GetReceiverFn(scope)
      .InvokesLambda(fn);
  }

}


declare module '../../../Common/LAMBDA/LAMBDA' {
  interface LAMBDA {
    HandlesSyncApi(action: string): LAMBDA;
  }
}
