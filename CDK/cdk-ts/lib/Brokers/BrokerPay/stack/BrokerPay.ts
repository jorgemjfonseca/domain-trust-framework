import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { BrokerTables } from '../../BrokerTables/stack/BrokerTables';

export interface BrokerPayDependencies {
  brokerTables: BrokerTables
}

/** 👉 https://quip.com/NBngAvaOflZ6#FIJABArj7az */
export class BrokerPay extends STACK {

  public static New(scope: Construct, deps: BrokerPayDependencies, props?: cdk.StackProps): BrokerPay {
    const ret = new BrokerPay(scope, props);
    ret.addDependency(deps.brokerTables);
    return ret;
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, BrokerPay.name, props);

    const wallets = BrokerTables.ImportWallets(this);

    LAMBDA
      .New(this, 'Charge')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .HandlesMessenger('Charge@Broker');

    LAMBDA
      .New(this, 'Subscribe')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .HandlesMessenger('Subscribe@Broker');

    LAMBDA
      .New(this, 'Resubscribe')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .HandlesMessenger('Resubscribe@Broker');

    LAMBDA
      .New(this, 'Unsubscribe')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .HandlesMessenger('Unsubscribe@Broker');

  }
}
