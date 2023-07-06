import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { SyncApiDkim } from '../../SyncApiDkim/stack/SyncApiDkim';
import { DomainName } from '../../DomainName/stack/DomainName';
import { Scope } from 'aws-cdk-lib/aws-ecs';

export interface SyncApiHandlersDependencies {
  syncApiDkim: SyncApiDkim
}

/** 👉 https://quip.com/RnO6Ad0BuBSx/-Sync-API */
export class SyncApiHandlers extends STACK {

  private static readonly MAP = 'SyncApiMap';

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
        .New(this, "Sender")
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
      .New(this, "Receiver")
      .ReadsFromDynamoDB(map, 'MAP')
      .InvokesLambda(dkimReaderFn, 'DKIM_READER_FN')
      .InvokesLambda(validatorFn, 'VALIDATOR_FN')
      .AddEnvironment('DOMAIN_NAME', domainName)
      .Export(SyncApiHandlers.RECEIVER);

    // REGISTER EXTENSIONS

    LAMBDA.prototype.HandlesSyncApi = 
      function(action: string, props?: HandlesSyncApiParameters) {
        SyncApiHandlers.HandlesSyncApi(this.Scope, action, this, props);
        return this;
      };

    LAMBDA.prototype.SendsSyncMessages = 
      function() {
        SyncApiHandlers.SendsSyncMessages(this.Scope, this);
        return this;
      };

  }
  


  public static HandlesSyncApi(
    scope: STACK, 
    action: string, 
    fn: LAMBDA, 
    props?: HandlesSyncApiParameters) 
  {
    const map = DYNAMO
      .Import(scope, SyncApiHandlers.MAP);
      
    // Register the function name.
    const ignoreValidation = props?.ignoreValidation 
      ? 'True' : 'False';
    map.PutItem({
      'ID': {'S':action},
      'Target': {'S':fn.FunctionName()},
      'IgnoreValidation': {'S':ignoreValidation}
    });

    // Authorize the receiver to invoke the function.
    SyncApiHandlers
      .GetReceiverFn(scope)
      .InvokesLambda(fn);
  }


  public static SendsSyncMessages(scope: STACK,fn: LAMBDA) {
    const sender = SyncApiHandlers.GetSenderFn(scope);
    fn.InvokesLambda(sender);
  }


}


interface HandlesSyncApiParameters {
  ignoreValidation?: boolean,
}


declare module '../../../Common/LAMBDA/LAMBDA' {
  interface LAMBDA {
    
    /** 👉 Registers the LAMBDA to be executed 
     * in response to synchronous requests from other domains. 
     * Details: https://quip.com/RnO6Ad0BuBSx/-Sync-API */
    HandlesSyncApi(action: string, props?: HandlesSyncApiParameters): LAMBDA;

    /** 👉 Authorizes the LAMBDA to send synchronous messages. 
     * Details: https://quip.com/RnO6Ad0BuBSx/-Sync-API */
    SendsSyncMessages(): LAMBDA;

  }

}
