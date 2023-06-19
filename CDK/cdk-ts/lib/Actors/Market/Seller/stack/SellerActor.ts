import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../../Common/LAMBDA/LAMBDA';
import { BUS } from '../../../../Common/BUS/BUS';
import { DYNAMO } from '../../../../Common/DYNAMO/DYNAMO';
import { SharedComms } from '../../../../Behaviours/SharedComms/stack/SharedComms';
import { STACK } from '../../../../Common/STACK/STACK';

// https://quip.com/U03QASVxXbhG/-Seller
export class SellerActor extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, SellerActor.name, props);

    const bus = BUS.Import(this, SharedComms.BUS);

    LAMBDA
      .New(this, 'PaidHandlerFn')
      .TriggeredByBus(bus, 'Seller-Paid')
      .PublishesToBus(bus);

  }
}
