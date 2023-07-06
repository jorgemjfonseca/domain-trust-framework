import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { BrokerTables } from '../../BrokerTables/stack/BrokerTables';

export interface BrokerBindsDependencies {
  brokerTables: BrokerTables
}

/** 👉 https://quip.com/oSzpA7HRICjq/-Broker-Binds */
export class BrokerBinds extends STACK {

  public static New(scope: Construct, deps:BrokerBindsDependencies, props?: cdk.StackProps): BrokerBinds {
    const ret = new BrokerBinds(scope, props);
    ret.addDependency(deps.brokerTables);
    return ret;
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, BrokerBinds.name, props);

    const wallets = BrokerTables.ImportWallets(this);
    const vaults = BrokerTables.ImportVaults(this);
    const binds = BrokerTables.ImportBinds(this);

    LAMBDA
      .New(this, 'Unbind')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .WritesToDynamoDB(binds, 'BINDS')
      .WritesToDynamoDB(vaults, 'VAULTS')
      .HandlesMessenger('Unbind@Broker');

    LAMBDA
      .New(this, 'Binds')
      .ReadsFromDynamoDB(wallets, 'WALLETS')
      .ReadsFromDynamoDB(binds, 'BINDS')
      .ReadsFromDynamoDB(vaults, 'VAULTS')
      .HandlesSyncApi('Binds@Broker');

    LAMBDA
      .New(this, 'Bindable')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .WritesToDynamoDB(binds, 'BINDS')
      .WritesToDynamoDB(vaults, 'VAULTS')
      .HandlesMessenger('Bindable@Broker')
      .SendsSyncMessages();

    LAMBDA
      .New(this, 'Bound')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .WritesToDynamoDB(binds, 'BINDS')
      .WritesToDynamoDB(vaults, 'VAULTS')
      .HandlesMessenger('Bound@Broker');

  }

}
