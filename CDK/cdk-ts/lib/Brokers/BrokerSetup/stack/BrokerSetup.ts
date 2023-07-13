import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DomainName } from '../../../Behaviours/DomainName/stack/DomainName';
import { BrokerTables } from '../../BrokerTables/stack/BrokerTables';

export interface BrokerSetupDependencies {
  domainName: DomainName,
  brokerTables: BrokerTables
}

/** 🤵📎 https://quip.com/zaYoA4kibXAP/-Broker-Setup */
export class BrokerSetup extends STACK {

  public static New (scope: Construct, deps: BrokerSetupDependencies, props?: cdk.StackProps): BrokerSetup {
    const ret = new BrokerSetup(scope, props);
    ret.addDependency(deps.brokerTables);
    return ret;
  }

  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, BrokerSetup.name, props);
      
    const wallets = BrokerTables.ImportWallets(this);
    const binds = BrokerTables.ImportBinds(this);
    const sessions = BrokerTables.ImportSessions(this);
    const credentials = BrokerTables.ImportCredentials(this);

    const queries = BrokerTables.ImportQueries(this);

    //doesn't compile
    //const rootDomain = DomainName.GetDomainName(this);
    LAMBDA
      .New(this, 'Onboard')
      .WritesToDynamoDB(wallets, 'WALLETS')
      //.AddEnvironment(rootDomain, 'DOMAIN')
      .HandlesSyncApi('Onboard@Broker')
    
    // 🧑‍🦰🐌 https://quip.com/zaYoA4kibXAP/-Broker-Setup#temp:C:DQN0cc419509625497ea39fa08e9
    LAMBDA
      .New(this, 'Translate')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .WritesToDynamoDB(sessions, 'SESSIONS')
      .WritesToDynamoDB(binds, 'BINDS')
      .WritesToDynamoDB(credentials, 'CREDENTIALS')
      .WritesToDynamoDB(queries, 'QUERIES')
      .HandlesMessenger('Translate@Broker', { ignoreValidation: true })
      .SendsSyncMessages() // Invoke Graph

  }

}
