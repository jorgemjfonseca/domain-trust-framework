import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { SQS } from '../../../Common/SQS/SQS';
import { STACK } from '../../../Common/STACK/STACK';
import { Domain } from '../../Domain/stack/Domain';

export interface PublisherDependencies {
  domain: Domain
}

//https://quip.com/sBavA8QtRpXu/-Publisher
export class Publisher extends STACK {

  public static New(scope: Construct, deps: PublisherDependencies, props?: cdk.StackProps)
  {
    const ret = new Publisher(scope, props);
    //ret.addDependency(deps.domain);
    return ret;
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, Publisher.name, props);

    const subscribers = DYNAMO
      .New(this, 'Subscribers');

    const updates = DYNAMO
      .New(this, 'Updates');

    const fanOutQueue = SQS
      .New(this, 'FanOutQueue');

    LAMBDA
      .New(this, 'FanOuter')
      .TriggeredBySQS(fanOutQueue)
      .PublishesToMessenger()

    const publishQueue = SQS
      .New(this, 'PublishQueue');

    LAMBDA
      .New(this, 'Publisher')
      .TriggeredBySQS(publishQueue)
      .ReadsFromDynamoDB(subscribers, 'SUBSCRIBERS')
      .PublishesToQueue(fanOutQueue, 'FANOUT');

    LAMBDA
      .New(this, 'Register')
      .WritesToDynamoDB(subscribers, 'SUBSCRIBERS')
      .HandlesMessenger('Publisher-Register');

    LAMBDA
      .New(this, 'Unregister')
      .WritesToDynamoDB(subscribers, 'SUBSCRIBERS')
      .HandlesMessenger('Publisher-Unregister');

    LAMBDA
      .New(this, 'Subscribe')
      .WritesToDynamoDB(subscribers, 'SUBSCRIBERS')
      .HandlesMessenger('Publisher-Subscribe');

    LAMBDA
      .New(this, 'Updated')
      .WritesToDynamoDB(updates, 'UPDATES')
      .PublishesToQueue(publishQueue, 'PUBLISHER')
      .HandlesMessenger('Publisher-Updated');

    LAMBDA
      .New(this, 'Replay')
      .WritesToDynamoDB(updates, 'UPDATES')
      .WritesToDynamoDB(subscribers, 'SUBSCRIBERS')
      .HandlesMessenger('Publisher-Replay');
      
  }
}
