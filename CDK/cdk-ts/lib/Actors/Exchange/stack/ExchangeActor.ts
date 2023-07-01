import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { VaultActor } from '../../Vault/stack/VaultActor';
import { STACK } from '../../../Common/STACK/STACK';

// https://quip.com/A5RYA3VoanVu/-Exchange
export class ExchangeActor extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, ExchangeActor.name, props);

    const binds = DYNAMO
      .Import(this, VaultActor.BINDS);

    const tills = DYNAMO
      .New(this, 'Tills');
      
    const counters = DYNAMO
      .New(this, 'Counters');

    const attendants = DYNAMO
      .New(this, 'Attendants');

  }
}
