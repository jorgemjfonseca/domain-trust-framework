import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { STACK } from '../../../Common/STACK/STACK';

// https://quip.com/EzmaAjGwmvRq/-Payer
export class PayerActor extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, PayerActor.name, props);

    const endorsements = DYNAMO
      .New(this, 'Endorsements');

    const collections = DYNAMO
      .New(this, 'Collections');

    LAMBDA
      .New(this, 'EndorseHandlerFn')
      .ReadsFromDynamoDB(endorsements, 'ENDORSEMENTS')
      .HandlesMessenger('Endorse@Payer');

    LAMBDA
      .New(this, 'CollectHandlerFn')
      .ReadsFromDynamoDB(collections, 'COLLECTIONS')
      .HandlesMessenger('Collect@Payer');

  }
}
