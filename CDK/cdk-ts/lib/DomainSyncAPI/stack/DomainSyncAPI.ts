import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { API } from '../../Common/ApiGW/Api';
import { LAMBDA } from '../../Common/Lambda/Lambda';
import { EXPRESS, STATES } from '../../Common/Workflow/Workflow';

export class DomainSyncAPI extends cdk.Stack {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, DomainSyncAPI.name, props);

    // IMPORTS
    const api = API.Import(this, "DomainApi");
    const wrapperFn = LAMBDA.Import(this, "DomainWrapperFn");
    const unwrapperFn = LAMBDA.Import(this, "DomainUnwrapperFn");

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
      .Export('SyncRouterApi')

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
