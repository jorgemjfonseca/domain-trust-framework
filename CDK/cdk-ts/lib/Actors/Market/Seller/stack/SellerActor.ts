import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../../Common/LAMBDA/LAMBDA';
import { STACK } from '../../../../Common/STACK/STACK';

// https://quip.com/U03QASVxXbhG/-Seller
export class SellerActor extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, SellerActor.name, props);

    LAMBDA
      .New(this, 'PaidHandlerFn')
      .HandlesMessenger('Seller-Paid');

  }
}
