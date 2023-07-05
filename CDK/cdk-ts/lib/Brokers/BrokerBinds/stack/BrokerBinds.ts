import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { Domain } from '../../../Behaviours/Domain/stack/Domain';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';


/** 👉 https://quip.com/oSzpA7HRICjq/-Broker-Binds */
export class BrokerBinds extends STACK {

  public static New(scope: Construct, props?: cdk.StackProps): BrokerBinds {
    const ret = new BrokerBinds(scope, props);
    return ret;
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, BrokerBinds.name, props);

    const vaults = DYNAMO.New(this, 'Vaults');
    const binds = DYNAMO.New(this, 'Binds');

    LAMBDA
      .New(this, 'Unbind')
      .WritesToDynamoDB(binds, 'BINDS')
      .ReadsFromDynamoDB(vaults, 'VAULTS')
      .HandlesMessenger('Unbind@Broker');

    LAMBDA
      .New(this, 'Binds')
      .ReadsFromDynamoDB(binds, 'BINDS')
      .ReadsFromDynamoDB(vaults, 'VAULTS')
      .HandlesSyncApi('Binds@Broker');

    LAMBDA
      .New(this, 'Bindable')
      .HandlesMessenger('Bindable@Broker');

    LAMBDA
      .New(this, 'Bound')
      .HandlesMessenger('Bound@Broker');

  }

}
