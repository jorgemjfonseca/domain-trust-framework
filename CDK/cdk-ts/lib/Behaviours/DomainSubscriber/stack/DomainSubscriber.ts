import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/Lambda/Lambda';
import { BUS } from '../../../Common/EventBus/EventBus';
import { DYNAMO } from '../../../Common/DynamoDB/DynamoDB';

//https://quip.com/9ab7AO56kkxY/-Subscriber
export class DomainSubscriber extends cdk.Stack {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, DomainSubscriber.name, props);

    const bus = BUS.Import(this, "DomainBus");

    const senderFn = LAMBDA
      .New(this, "SubscriberFn")
      .TriggeredByBus(bus, ['DTFW'], ['PUBLISH'])
      .PublishesToBus(bus)
      .WritesToDynamoDB(DYNAMO.New(this, "Deduplication"));

  }
}
