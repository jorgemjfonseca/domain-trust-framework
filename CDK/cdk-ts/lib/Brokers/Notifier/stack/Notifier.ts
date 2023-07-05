import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { Domain } from '../../../Behaviours/Domain/stack/Domain';


export interface NotifierDependencies {
  domain: Domain
}


/** 👉 https://quip.com/PCunAKUqSObO/-Notifier */
export class Notifier extends STACK {

  public static New(scope: Construct, deps: NotifierDependencies, props?: cdk.StackProps): Notifier {
    const ret = new Notifier(scope, props);
    ret.addDependency(deps.domain);
    return ret;
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, Notifier.name, props);

    const wallets = DYNAMO.New(this, 'Wallets');

    LAMBDA
      .New(this, 'Onboard')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .HandlesSyncApi('Onboard@Notifier');

    LAMBDA
      .New(this, 'Translated')
      .ReadsFromDynamoDB(wallets, 'WALLETS')
      .HandlesMessenger('Translated@Notifier');

    LAMBDA
      .New(this, 'Updated')
      .WritesToDynamoDB(wallets, 'WALLETS')
      .HandlesMessenger('Updated@Notifier');

    LAMBDA
      .New(this, 'Prompt')
      .ReadsFromDynamoDB(wallets, 'WALLETS')
      .HandlesMessenger('Prompt@Notifier');

    LAMBDA
      .New(this, 'Bindable')
      .ReadsFromDynamoDB(wallets, 'WALLETS')
      .HandlesMessenger('Bindable@Notifier');

    LAMBDA
      .New(this, 'Bound')
      .ReadsFromDynamoDB(wallets, 'WALLETS')
      .HandlesMessenger('Bound@Notifier');

    LAMBDA
      .New(this, 'Issued')
      .ReadsFromDynamoDB(wallets, 'WALLETS')
      .HandlesMessenger('Issued@Notifier');

    LAMBDA
      .New(this, 'Revoked')
      .ReadsFromDynamoDB(wallets, 'WALLETS')
      .HandlesMessenger('Revoked@Notifier');

    LAMBDA
      .New(this, 'Query')
      .ReadsFromDynamoDB(wallets, 'WALLETS')
      .HandlesMessenger('Query@Notifier');

    LAMBDA
      .New(this, 'Charge')
      .ReadsFromDynamoDB(wallets, 'WALLETS')
      .HandlesMessenger('Charge@Notifier');
  }

}
