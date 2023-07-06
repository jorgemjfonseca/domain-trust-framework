import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { BrokerTables } from '../../BrokerTables/stack/BrokerTables';

export interface BrokerCredentialsDependencies {
  brokerTables: BrokerTables
}

/** 👉 https://quip.com/sN8DACFLN9wM#AfTABAujlEx */
export class BrokerCredentials extends STACK {

  public static New(scope: Construct, deps: BrokerCredentialsDependencies, props?: cdk.StackProps): BrokerCredentials {
    const ret = new BrokerCredentials(scope, props);
    ret.addDependency(deps.brokerTables);
    return ret;
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, BrokerCredentials.name, props);

    const wallets = BrokerTables.ImportWallets(this);
    const issuers = BrokerTables.ImportIssuers(this);
    const credentials = BrokerTables.ImportCredentials(this);

    LAMBDA
      .New(this, 'Issue')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .WritesToDynamoDB(issuers, 'ISSUERS')
      .WritesToDynamoDB(credentials, 'CREDENTIALS')
      .HandlesMessenger('Issue@Broker');

    LAMBDA  
      .New(this, 'Revoke')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .WritesToDynamoDB(issuers, 'ISSUERS')
      .WritesToDynamoDB(credentials, 'CREDENTIALS')
      .HandlesMessenger('Revoke@Broker');

    LAMBDA
      .New(this, 'Accepted')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .WritesToDynamoDB(issuers, 'ISSUERS')
      .WritesToDynamoDB(credentials, 'CREDENTIALS')
      .HandlesMessenger('Accepted@Broker');

    LAMBDA
      .New(this, 'Credentials')
      .ReadsFromDynamoDB(wallets, 'WALLETS')
      .ReadsFromDynamoDB(issuers, 'ISSUERS')
      .ReadsFromDynamoDB(credentials, 'CREDENTIALS')
      .HandlesSyncApi('Credentials@Broker');

    LAMBDA
      .New(this, 'Remove')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .WritesToDynamoDB(issuers, 'ISSUERS')
      .WritesToDynamoDB(credentials, 'CREDENTIALS')
      .HandlesMessenger('Remove@Broker');


  }
}
