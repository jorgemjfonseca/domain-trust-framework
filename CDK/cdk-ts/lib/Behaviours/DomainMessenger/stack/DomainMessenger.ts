import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { API } from '../../../Common/ApiGW/Api';
import { QUEUE } from '../../../Common/Queue/Queue';
import { LAMBDA } from '../../../Common/Lambda/Lambda';
import { EXPRESS, STANDARD, STATES } from '../../../Common/Workflow/Workflow';
import { BUS } from '../../../Common/EventBus/EventBus';

//https://quip.com/Fxj4AdnE6Eu5/-Messenger
export class DomainMessenger extends cdk.Stack {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, DomainMessenger.name, props);
   
    // IMPORTS
    const bus = BUS.Import(this, "DomainBus");
    const api = API.Import(this, "DomainApi");
    const wrapperFn = LAMBDA.Import(this, "DomainWrapperFn");
    const unwrapperFn = LAMBDA.Import(this, "DomainUnwrapperFn");

    // SENDER FUNCTION 
    const senderFn = LAMBDA.New(this, "SenderFn");

    // SENDER WORKFLOW
    STANDARD
      .New(this, "SenderWf", 
        new STATES(this, 'SenderWfDef')
          .InvokeLambda(wrapperFn)
          .ThenInvokeLambda(senderFn)
          .ThenSuccess())
      .TriggeredByBus(bus, { 
        source: ['OutboundDomainMessages'] 
      });

    // PUBLISHER FUNCTION
    const publisherFn = 
      LAMBDA.New(this, "PublisherFn")
        .PublishesToBus(bus);

    // RECEIVER WORKFLOW
    const receiverWf = STANDARD.New(this, "ReceiverWf",
      new STATES(this, "ReceiverWfDef")
        .InvokeLambda(unwrapperFn)
        .ThenInvokeLambda(publisherFn)
        .ThenSuccess()
      );

    // RECEIVER FUNCTION
    const receiverFn = 
      LAMBDA.New(this, "ReceiverFn")
        .AddApiMethod(api, "async")
        .TriggersWorkflow(receiverWf);

  }
}

