import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { BUS } from '../../../Common/BUS/BUS';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { SharedComms } from '../../SharedComms/stack/SharedComms';
import { SQS } from '../../../Common/SQS/SQS';
import { STACK } from '../../../Common/STACK/STACK';

//https://quip.com/sBavA8QtRpXu/-Publisher
export class PublisherBehaviour extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, PublisherBehaviour.name, props);

    const bus = BUS
      .Import(this, SharedComms.BUS);

    const subscribers = DYNAMO
      .New(this, 'Subscribers');

    const updates = DYNAMO
      .New(this, 'Updates');

    const fanOutQueue = SQS
      .New(this, 'FanOutQueue');

    LAMBDA
      .New(this, 'FanOuterFn')
      .TriggeredByQueue(fanOutQueue);

    const publishQueue = SQS
      .New(this, 'PublishQueue');

    LAMBDA
      .New(this, 'PublisherFn')
      .TriggeredByQueue(publishQueue)
      .ReadsFromDynamoDBs([ subscribers ])
      .PublishesToQueue(fanOutQueue);

    LAMBDA
      .New(this, 'RegisterHandlerFn')
      .SpeaksWithBus(bus, 'Publisher-Register')
      .WritesToDynamoDBs([ subscribers ]);

    LAMBDA
      .New(this, 'UnregisterHandlerFn')
      .SpeaksWithBus(bus, 'Publisher-Unregister')
      .WritesToDynamoDBs([ subscribers ]);

    LAMBDA
      .New(this, 'SubscribeHandlerFn')
      .SpeaksWithBus(bus, 'Publisher-Subscribe')
      .WritesToDynamoDBs([ subscribers ]);

    LAMBDA
      .New(this, 'UpdatedHandlerFn')
      .SpeaksWithBus(bus, 'Publisher-Updated')
      .WritesToDynamoDBs([ updates ])
      .PublishesToQueue(publishQueue);

    LAMBDA
      .New(this, 'ReplayHandlerFn')
      .SpeaksWithBus(bus, 'Publisher-Replay')
      .WritesToDynamoDBs([ updates, subscribers ]);
      
  }
}
