import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { API } from '../../../Common/API/API';
import { SQS } from '../../../Common/SQS/SQS';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { EXPRESS, STANDARD, STATES } from '../../../Common/WORKFLOW/WORKFLOW';
import { BUS } from '../../../Common/BUS/BUS';
import { SharedComms } from '../../SharedComms/stack/SharedComms';
import { STACK } from '../../../Common/STACK/STACK';

//https://quip.com/Fxj4AdnE6Eu5/-Messenger
export class MessengerBehaviour extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, MessengerBehaviour.name, props);
   
    // IMPORTS
    const bus = BUS.Import(this, SharedComms.BUS);
    const api = API.Import(this, SharedComms.API);
    const wrapperFn = LAMBDA.Import(this, SharedComms.WRAPPER);
    const unwrapperFn = LAMBDA.Import(this, SharedComms.UNWRAPPER);

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
      LAMBDA.New(this, "WebHookFn")
        .AddApiMethod(api, "async")
        .TriggersWorkflow(receiverWf);

  }
}

