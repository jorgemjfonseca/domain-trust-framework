import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { API } from '../../Common/ApiGW/Api';
import { QUEUE } from '../../Common/Queue/Queue';
import { LAMBDA } from '../../Common/Lambda/Lambda';
import { EXPRESS, STANDARD, WORKFLOW } from '../../Common/Workflow/Workflow';
import { BUS } from '../../Common/EventBus/EventBus';

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

    // SENDER MACHINE
    EXPRESS
      .New(this, "SenderWf", 
        new WORKFLOW(this, 'Prod')
          .InvokeLambda(wrapperFn)
          .ThenInvokeLambda(senderFn)
          .ThenSuccess())
      .TriggeredByEventBus(bus, { 
        source: ['OutboundDomainMessages'] 
      });
   
    // SENDER MACHINE
    STANDARD
      .New(this, "SenderWfTest", 
        new WORKFLOW(this, 'Test')
          .InvokeLambda(wrapperFn)
          .ThenInvokeLambda(senderFn)
          .ThenSuccess())
      .TriggeredByEventBus(bus, { 
        source: ['OutboundDomainMessages'] 
      });

    // RECEIVER QUEUE
    const receiverQueue = QUEUE.New(this, 'ReceiverQueue');

  }
}

