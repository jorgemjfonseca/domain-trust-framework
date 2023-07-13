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

    const wallets = DYNAMO
      .New(this, 'Wallets')
      .Export('BROKER_WALLETS');

    const sessions = DYNAMO
      .New(this, 'Sessions')
      .AddIndex('WalletID')
      .Export('BROKER_SESSIONS');

    const binds = DYNAMO
      .New(this, 'Binds')
      .AddIndex('WalletID')
      .Export('BROKER_BINDS');

    const credentials = DYNAMO
      .New(this, 'Credentials')
      .AddIndex('WalletID')
      .Export('BROKER_CREDENTIALS')

    const queries = DYNAMO
      .New(this, 'Queries')
      .Export('BROKER_QUERIES')
    
  }

  public static ImportWallets(stack: STACK): DYNAMO {
    return DYNAMO.Import(stack, 'BROKER_WALLETS');
  }

  public static ImportSessions(stack: STACK): DYNAMO {
    return DYNAMO.Import(stack, 'BROKER_SESSIONS');
  }

  public static ImportBinds(stack: STACK): DYNAMO {
    return DYNAMO.Import(stack, 'BROKER_BINDS');
  }

  public static ImportCredentials(stack: STACK): DYNAMO {
    return DYNAMO.Import(stack, 'BROKER_CREDENTIALS');
  }

  public static ImportQueries(stack: STACK): DYNAMO {
    return DYNAMO.Import(stack, 'BROKER_QUERIES');
  }

}
