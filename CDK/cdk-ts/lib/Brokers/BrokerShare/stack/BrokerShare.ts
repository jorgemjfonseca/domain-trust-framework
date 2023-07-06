import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { BrokerTables } from '../../BrokerTables/stack/BrokerTables';

export interface BrokerShareDependencies {
  brokerTables: BrokerTables
}

/** 👉 https://quip.com/rKzMApUS5QIi#WTIABAsxxkW */
export class BrokerShare extends STACK {

  public static New (scope: Construct, deps: BrokerShareDependencies, props?: cdk.StackProps): BrokerShare {
    const ret = new BrokerShare(scope, props);
    ret.addDependency(deps.brokerTables);
    return ret;
  }

  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, BrokerShare.name, props);

    const wallets = BrokerTables.ImportWallets(this);
    const queries = BrokerTables.ImportQueries(this);

    LAMBDA
      .New(this, 'Query')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .WritesToDynamoDB(queries, 'QUERIES')
      .HandlesMessenger('Query@Broker')

  }

}
