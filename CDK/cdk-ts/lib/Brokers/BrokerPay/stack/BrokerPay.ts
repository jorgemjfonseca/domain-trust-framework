import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';


/** 👉 https://quip.com/NBngAvaOflZ6#FIJABArj7az */
export class BrokerPay extends STACK {

  public static New(scope: Construct, props?: cdk.StackProps): BrokerPay {
    const ret = new BrokerPay(scope, props);
    return ret;
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, BrokerPay.name, props);

    LAMBDA
      .New(this, 'Charge')
      .HandlesMessenger('Charge@Broker');

    LAMBDA
      .New(this, 'Subscribe')
      .HandlesMessenger('Subscribe@Broker');

    LAMBDA
      .New(this, 'Resubscribe')
      .HandlesMessenger('Resubscribe@Broker');

    LAMBDA
      .New(this, 'Unsubscribe')
      .HandlesMessenger('Unsubscribe@Broker');

  }
}
