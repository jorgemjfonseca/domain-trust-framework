import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DomainName } from '../../../Behaviours/DomainName/stack/DomainName';
import { BrokerTables } from '../../BrokerTables/stack/BrokerTables';

export interface BrokerSetupDependencies {
  domainName: DomainName,
  brokerTables: BrokerTables
}

/** 👉 https://quip.com/zaYoA4kibXAP/-Broker-Setup */
export class BrokerSetup extends STACK {

  public static New (scope: Construct, deps: BrokerSetupDependencies, props?: cdk.StackProps): BrokerSetup {
    const ret = new BrokerSetup(scope, props);
    ret.addDependency(deps.brokerTables);
    return ret;
  }

  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, BrokerSetup.name, props);
      
    const wallets = BrokerTables.ImportWallets(this);
    const locators = BrokerTables.ImportLocators(this);

    const binds = BrokerTables.ImportBinds(this);
    const vaults = BrokerTables.ImportVaults(this);

    const hosts = BrokerTables.ImportHosts(this);
    const sessions = BrokerTables.ImportSessions(this);

    const issuers = BrokerTables.ImportIssuers(this);
    const credentials = BrokerTables.ImportCredentials(this);

    const queries = BrokerTables.ImportQueries(this);

    //doesn't compile
    //const rootDomain = DomainName.GetDomainName(this);
    LAMBDA
      .New(this, 'Onboard')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .WritesToDynamoDB(locators, 'LOCATORS')
      //.AddEnvironment(rootDomain, 'DOMAIN')
      .HandlesSyncApi('Onboard@Broker')

    LAMBDA
      .New(this, 'Translate')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .WritesToDynamoDB(hosts, 'HOSTS')
      .WritesToDynamoDB(sessions, 'SESSIONS')
      .WritesToDynamoDB(vaults, 'VAULTS')
      .WritesToDynamoDB(binds, 'BINDS')
      .WritesToDynamoDB(issuers, 'ISSUERS')
      .WritesToDynamoDB(credentials, 'CREDENTIALS')
      .WritesToDynamoDB(queries, 'QUERIES')
      .HandlesMessenger('Translate@Broker')
      .SendsSyncMessages() // Invoke Graph

    LAMBDA
      .New(this, 'Replace')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .HandlesSyncApi('Replace@Broker')

    LAMBDA
      .New(this, 'QR')
      .ReadsFromDynamoDB(wallets, 'WALLETS')
      .HandlesSyncApi('QR@Broker')

  }

}
