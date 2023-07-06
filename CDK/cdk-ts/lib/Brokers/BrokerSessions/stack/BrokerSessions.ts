import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { BrokerTables } from '../../BrokerTables/stack/BrokerTables';

export interface BrokerSessionsDependencies {
  brokerTables: BrokerTables
}

/** 👉 https://quip.com/HrgkAuQCqBez#bXDABAe5brB */
export class BrokerSessions extends STACK {

  public static New(scope: Construct, deps: BrokerSessionsDependencies, props?: cdk.StackProps): BrokerSessions {
    const ret = new BrokerSessions(scope, props);
    ret.addDependency(deps.brokerTables);
    return ret;
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, BrokerSessions.name, props);

    const wallets = BrokerTables.ImportWallets(this);
    const hosts = BrokerTables.ImportHosts(this);
    const sessions = BrokerTables.ImportSessions(this);

    LAMBDA
      .New(this, 'Sessions')
      .ReadsFromDynamoDB(wallets, 'WALLETS')
      .ReadsFromDynamoDB(hosts, 'HOSTS')
      .ReadsFromDynamoDB(sessions, 'SESSIONS')
      .HandlesSyncApi('Sessions@Broker')

    LAMBDA
      .New(this, 'Talker')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .WritesToDynamoDB(hosts, 'HOSTS')
      .WritesToDynamoDB(sessions, 'SESSIONS')
      .HandlesMessenger('Talker@Broker');

    LAMBDA
      .New(this, 'Checkout')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .WritesToDynamoDB(hosts, 'HOSTS')
      .WritesToDynamoDB(sessions, 'SESSIONS')
      .HandlesMessenger('Checkout@Broker');

    LAMBDA
      .New(this, 'Abandon')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .WritesToDynamoDB(hosts, 'HOSTS')
      .WritesToDynamoDB(sessions, 'SESSIONS')
      .HandlesMessenger('Abandon@Broker');

    LAMBDA
      .New(this, 'Assess')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .WritesToDynamoDB(hosts, 'HOSTS')
      .WritesToDynamoDB(sessions, 'SESSIONS')
      .HandlesSyncApi('Assess@Broker');

    LAMBDA
      .New(this, 'Goodbye')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .WritesToDynamoDB(hosts, 'HOSTS')
      .WritesToDynamoDB(sessions, 'SESSIONS')
      .HandlesMessenger('Goodbye@Broker');
  }

}
