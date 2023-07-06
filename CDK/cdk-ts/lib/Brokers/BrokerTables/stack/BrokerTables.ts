import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';


/** 👉 https://quip.com/oSzpA7HRICjq/-Broker-Binds */
export class BrokerTables extends STACK {

  public static New(scope: Construct, props?: cdk.StackProps): BrokerTables {
    const ret = new BrokerTables(scope, props);
    return ret;
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, BrokerTables.name, props);

    const wallets = DYNAMO.New(this, 'Wallets').Export('BROKER_WALLETS');
    const locators = DYNAMO.New(this, 'Locators').Export('BROKER_LOCATORS');

    const hosts = DYNAMO.New(this, 'Hosts', { filtered: true }).Export('BROKER_HOSTS');
    const sessions = DYNAMO.New(this, 'Sessions', { filtered: true }).Export('BROKER_SESSIONS');

    const vaults = DYNAMO.New(this, 'Vaults').Export('BROKER_VAULTS');
    const binds = DYNAMO.New(this, 'Binds').Export('BROKER_BINDS');

    const issuers = DYNAMO.New(this, 'Issuers').Export('BROKER_ISSUERS');
    const credentials = DYNAMO.New(this, 'Credentials').Export('BROKER_CREDENTIALS')

    const queries = DYNAMO.New(this, 'Queries').Export('BROKER_QUERIES')
    
  }

  public static ImportWallets(stack: STACK): DYNAMO {
    return DYNAMO.Import(stack, 'BROKER_WALLETS');
  }

  public static ImportLocators(stack: STACK): DYNAMO {
    return DYNAMO.Import(stack, 'BROKER_LOCATORS');
  }

  public static ImportHosts(stack: STACK): DYNAMO {
    return DYNAMO.Import(stack, 'BROKER_HOSTS');
  }

  public static ImportSessions(stack: STACK): DYNAMO {
    return DYNAMO.Import(stack, 'BROKER_SESSIONS');
  }

  public static ImportVaults(stack: STACK): DYNAMO {
    return DYNAMO.Import(stack, 'BROKER_VAULTS');
  }

  public static ImportBinds(stack: STACK): DYNAMO {
    return DYNAMO.Import(stack, 'BROKER_BINDS');
  }

  public static ImportIssuers(stack: STACK): DYNAMO {
    return DYNAMO.Import(stack, 'BROKER_ISSUERS');
  }

  public static ImportCredentials(stack: STACK): DYNAMO {
    return DYNAMO.Import(stack, 'BROKER_CREDENTIALS');
  }

  public static ImportQueries(stack: STACK): DYNAMO {
    return DYNAMO.Import(stack, 'BROKER_QUERIES');
  }

}
