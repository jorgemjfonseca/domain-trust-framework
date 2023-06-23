import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { STACK } from '../../../Common/STACK/STACK';

//https://quip.com/9ab7AO56kkxY/-Subscriber
export class SubscriberBehaviour extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, SubscriberBehaviour.name, props);

    const dedups = DYNAMO
      .New(this, "Deduplication");

    const senderFn = LAMBDA
      .New(this, "SubscriberFn")
      .WritesToDynamoDB(dedups)
      .HandlesMessenger('Subscriber-Publish');
;

  }
}
