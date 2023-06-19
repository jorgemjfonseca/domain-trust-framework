import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { API } from '../../../Common/API/API';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { EXPRESS, STATES } from '../../../Common/WORKFLOW/WORKFLOW';
import { SharedComms } from '../../SharedComms/stack/SharedComms';
import { STACK } from '../../../Common/STACK/STACK';

//https://quip.com/RnO6Ad0BuBSx/-Sync-API
export class SyncApiBehaviour extends STACK {

  public static readonly ROUTER = 'SyncRouterApi';

  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, SyncApiBehaviour.name, props);

    // IMPORTS
    const api = API.Import(this, SharedComms.API);
    const wrapperFn = LAMBDA.Import(this, SharedComms.WRAPPER);
    const unwrapperFn = LAMBDA.Import(this, SharedComms.UNWRAPPER);

    // SENDER FUNCTION 
    const senderFn = LAMBDA.New(this, "SenderFn");

    // SENDER WORKFLOW
    EXPRESS
      .New(this, "SenderWf", 
        new STATES(this, 'SenderWfDef')
          .InvokeLambda(wrapperFn)
          .ThenInvokeLambda(senderFn)
          .ThenSuccess());

    const routerApi = API
      .New(this, 'RouterApi')
      .Export(SyncApiBehaviour.ROUTER)

    // ROUTER FUNCTION
    const routerFn = LAMBDA
      .New(this, "RouterFn")
      .AddEnvironment("ROUTER_ENDPOINT", routerApi.Super.url);

    // RECEIVER WORKFLOW
    const receiverWf = EXPRESS
      .New(this, "ReceiverWf", STATES
        .New(this, "ReceiverWfDef")
        .InvokeLambda(unwrapperFn)
        .ThenInvokeLambda(routerFn)
        .ThenSuccess()
      );

    // RECEIVER FUNCTION
    const receiverFn = 
      LAMBDA.New(this, "ReceiverFn")
        .AddApiMethod(api, "sync")
        .TriggersWorkflow(receiverWf);
   
  }
}
