import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { BUS } from '../../../Common/BUS/BUS';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { SharedComms } from '../../SharedComms/stack/SharedComms';
import { STACK } from '../../../Common/STACK/STACK';

//https://quip.com/9ab7AO56kkxY/-Subscriber
export class SubscriberBehaviour extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, SubscriberBehaviour.name, props);

    const bus = BUS.Import(this, SharedComms.BUS);

    const senderFn = LAMBDA
      .New(this, "SubscriberFn")
      .TriggeredByBus(bus, 'Subscriber.Publish')
      .PublishesToBus(bus)
      .WritesToDynamoDB(DYNAMO.New(this, "Deduplication"));

  }
}
