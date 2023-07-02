import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { STACK } from '../../../Common/STACK/STACK';

// https://quip.com/TkhkAIHSg8Pp/-Collector
export class CollectorActor extends STACK {

  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, CollectorActor.name, props);

    const collections = DYNAMO
      .New(this, 'Collections');
      
    const refunds = DYNAMO
      .New(this, 'Refunds');

    LAMBDA
      .New(this, 'CollectHandlerFn')
      .WritesToDynamoDB(collections, 'COLLECTIONS')
      .HandlesMessenger('Collect@Collector');

    LAMBDA
      .New(this, 'RefundHandlerFn')
      .WritesToDynamoDB(refunds, 'REFUNDS')
      .HandlesMessenger('Refund@Collector');

    LAMBDA
      .New(this, 'UnsubscribeHandlerFn')
      .HandlesSyncApi('Unsubscribe@Collector');

  }
}
