import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';


/** 👉 https://quip.com/zaYoA4kibXAP/-Broker-Setup */
export class BrokerSetup extends STACK {

  public static New (scope: Construct, props?: cdk.StackProps): BrokerSetup {
    return new BrokerSetup(scope, props);
  }

  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, BrokerSetup.name, props);

    const wallets = DYNAMO.New(this, 'Wallets')

    LAMBDA
      .New(this, 'Onboard')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .HandlesSyncApi('Onboard@Broker')

    LAMBDA
      .New(this, 'Translate')
      .ReadsFromDynamoDB(wallets, 'WALLETS')
      .HandlesSyncApi('Translate@Broker')

    LAMBDA
      .New(this, 'Replace')
      .WritesToDynamoDB(wallets, 'WALLETS')

    LAMBDA
      .New(this, 'QR')
      .ReadsFromDynamoDB(wallets, 'WALLETS')

  }

}
