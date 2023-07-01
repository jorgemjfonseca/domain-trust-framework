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
      .New(this, "Deduplication");

    LAMBDA
      .New(this, "ConfirmFn")
      .HandlesMessenger('Subscriber-Confirm');

    LAMBDA
      .New(this, "ConsumeFn")
      .WritesToDynamoDB(dedups, 'DEDUPS')
      .HandlesMessenger('Subscriber-Consume');

    LAMBDA
      .New(this, "UpdatedFn")
      .WritesToDynamoDB(dedups, 'DEDUPS')
      .HandlesMessenger('Subscriber-Updated');
  }
}
