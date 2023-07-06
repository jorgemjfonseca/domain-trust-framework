import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { BrokerTables } from '../../BrokerTables/stack/BrokerTables';

export interface BrokerPromptDependencies {
  brokerTables: BrokerTables
}

/** 👉 https://quip.com/FNbzAVSVu9z6#RCPABAYylHR */
export class BrokerPrompt extends STACK {

  public static New(scope: Construct, deps: BrokerPromptDependencies, props?: cdk.StackProps): BrokerPrompt {
    const ret = new BrokerPrompt(scope, props);
    ret.addDependency(deps.brokerTables);
    return ret;
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, BrokerPrompt.name, props);

    const wallets = BrokerTables.ImportWallets(this);

    LAMBDA
      .New(this, 'Prompt')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .HandlesMessenger('Prompt@Broker');

  }

}
