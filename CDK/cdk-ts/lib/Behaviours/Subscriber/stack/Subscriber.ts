import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { STACK } from '../../../Common/STACK/STACK';

//https://quip.com/9ab7AO56kkxY/-Subscriber
export class Subscriber extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, Subscriber.name, props);

    const dedups = DYNAMO
      .New(this, "Deduplication", {
        ttl: "TTL"
      });

    LAMBDA
      .New(this, "Confirm")
      .HandlesMessenger('Subscriber-Confirm');

    LAMBDA
      .New(this, "Consume")
      .WritesToDynamoDB(dedups, 'DEDUPS')
      .HandlesMessenger('Subscriber-Consume');

    LAMBDA
      .New(this, "Updated")
      .WritesToDynamoDB(dedups, 'DEDUPS')
      .HandlesMessenger('Subscriber-Updated');
  }
}
