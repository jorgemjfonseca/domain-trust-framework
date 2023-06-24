import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { SQS } from '../../../Common/SQS/SQS';
import { STACK } from '../../../Common/STACK/STACK';

//https://quip.com/sBavA8QtRpXu/-Publisher
export class Publisher extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, Publisher.name, props);

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
      .ReadsFromDynamoDB(subscribers)
      .PublishesToQueue(fanOutQueue);

    LAMBDA
      .New(this, 'RegisterHandlerFn')
      .WritesToDynamoDB(subscribers)
      .HandlesMessenger('Publisher-Register');

    LAMBDA
      .New(this, 'UnregisterHandlerFn')
      .WritesToDynamoDB(subscribers)
      .HandlesMessenger('Publisher-Unregister');

    LAMBDA
      .New(this, 'SubscribeHandlerFn')
      .WritesToDynamoDB(subscribers)
      .HandlesMessenger('Publisher-Subscribe');

    LAMBDA
      .New(this, 'UpdatedHandlerFn')
      .WritesToDynamoDB(updates)
      .PublishesToQueue(publishQueue)
      .HandlesMessenger('Publisher-Updated');

    LAMBDA
      .New(this, 'ReplayHandlerFn')
      .WritesToDynamoDB(updates, 'UPDATES')
      .WritesToDynamoDB(subscribers, 'SUBSCRIBERS')
      .HandlesMessenger('Publisher-Replay');
      
  }
}
