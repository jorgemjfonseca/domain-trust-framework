import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { BrokerTables } from '../../BrokerTables/stack/BrokerTables';

export interface BrokerSessionsDependencies {
  brokerTables: BrokerTables
}

/** 🤵📎 https://quip.com/HrgkAuQCqBez#bXDABAe5brB */
export class BrokerSessions extends STACK {

  public static New(scope: Construct, deps: BrokerSessionsDependencies, props?: cdk.StackProps): BrokerSessions {
    const ret = new BrokerSessions(scope, props);
    ret.addDependency(deps.brokerTables);
    return ret;
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, BrokerSessions.name, props);

    const wallets = BrokerTables.ImportWallets(this);
    const domains = BrokerTables.ImportDomains(this);
    const domainTranslations = BrokerTables.ImportDomainTranslations(this);
    const sessions = BrokerTables.ImportSessions(this);

    // 🧑‍🦰🚀 https://quip.com/HrgkAuQCqBez/-Broker-Sessions#temp:C:bXD09ae7595fe4943d5985d83fd0
    LAMBDA
      .New(this, 'Sessions')
      .ReadsFromDynamoDB(wallets, 'WALLETS')
      .ReadsFromDynamoDB(domains, 'DOMAINS')
      .ReadsFromDynamoDB(domainTranslations, 'DOMAIN_TRANSLATIONS')
      .ReadsFromDynamoDB(sessions, 'SESSIONS')
      .HandlesSyncApi('Sessions@Broker', { ignoreValidation: true })

    // 🧑‍🦰🐌 https://quip.com/HrgkAuQCqBez/-Broker-Sessions#temp:C:bXDff3472e2ec4d4733bd1b38141
    LAMBDA
      .New(this, 'Talker')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .ReadsFromDynamoDB(domains, 'DOMAINS')
      .ReadsFromDynamoDB(domainTranslations, 'DOMAIN_TRANSLATIONS')
      .WritesToDynamoDB(sessions, 'SESSIONS')
      .HandlesMessenger('Talker@Broker', { ignoreValidation: true });

    // 🧑‍🦰🐌 https://quip.com/HrgkAuQCqBez/-Broker-Sessions#temp:C:bXDca9dada42bf6431daed5f1c07
    LAMBDA
      .New(this, 'Checkout')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .ReadsFromDynamoDB(domains, 'DOMAINS')
      .ReadsFromDynamoDB(domainTranslations, 'DOMAIN_TRANSLATIONS')
      .WritesToDynamoDB(sessions, 'SESSIONS')
      .HandlesMessenger('Checkout@Broker', { ignoreValidation: true });

    // 🧑‍🦰🐌 https://quip.com/HrgkAuQCqBez/-Broker-Sessions#temp:C:bXD2d6cd3790047405c89019c170
    LAMBDA
      .New(this, 'Abandon')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .ReadsFromDynamoDB(domains, 'DOMAINS')
      .ReadsFromDynamoDB(domainTranslations, 'DOMAIN_TRANSLATIONS')
      .WritesToDynamoDB(sessions, 'SESSIONS')
      .HandlesMessenger('Abandon@Broker', { ignoreValidation: true });

    // 🧑‍🦰🚀 https://quip.com/HrgkAuQCqBez/-Broker-Sessions#temp:C:bXD4396f26fefe34874a12828c36
    LAMBDA
      .New(this, 'Assess')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .WritesToDynamoDB(domains, 'DOMAINS')
      .WritesToDynamoDB(domainTranslations, 'DOMAIN_TRANSLATIONS')
      .WritesToDynamoDB(sessions, 'SESSIONS')
      .HandlesSyncApi('Assess@Broker', { ignoreValidation: true });

    // 🤗🐌 https://quip.com/HrgkAuQCqBez/-Broker-Sessions#temp:C:bXD9f09e5f058ee4fc8a77be4ebe
    LAMBDA
      .New(this, 'Goodbye')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .ReadsFromDynamoDB(domains, 'DOMAINS')
      .ReadsFromDynamoDB(domainTranslations, 'DOMAIN_TRANSLATIONS')
      .WritesToDynamoDB(sessions, 'SESSIONS')
      .HandlesMessenger('Goodbye@Broker');
  }

}
