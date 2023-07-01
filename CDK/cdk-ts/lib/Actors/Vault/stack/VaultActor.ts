import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { STACK } from '../../../Common/STACK/STACK';

// https://quip.com/IZapAfPZPnOD
export class VaultActor extends STACK {

  private static readonly DISCLOSE_FN = 'Vault-DiscloseHandlerFn';
  public static readonly BINDS = 'Vault-BindsTable';
  public static readonly WALLETS = 'Vault-WalletsTable';

  private discloseFn: LAMBDA;
  public GetDiscloseFn() {
    return this.discloseFn;
  }

  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, VaultActor.name, props);

    const wallets = DYNAMO
      .New(this, 'Wallets')
      .Export(VaultActor.WALLETS);

    const binds = DYNAMO
      .New(this, 'Binds')
      .Export(VaultActor.BINDS);

    const disclosures = DYNAMO
      .New(this, 'Disclosures');

    const grants = DYNAMO
      .New(this, 'Grants');

    LAMBDA
      .New(this, 'BindHandlerFn')
      .WritesToDynamoDB(binds, 'BINDS')
      .HandlesMessenger('Vault-Bind');

    this.discloseFn = LAMBDA
      .New(this, 'DiscloseHandlerFn')
      .WritesToDynamoDB(disclosures, 'DISCLOSURES')
      .HandlesMessenger('Vault-Disclose')
      .Export(VaultActor.DISCLOSE_FN);

    LAMBDA
      .New(this, 'ContinueHandlerFn')
      .HandlesMessenger('Vault-Continue');

    LAMBDA
      .New(this, 'UnbindHandlerFn')
      .HandlesMessenger('Vault-Unbind');

    LAMBDA
      .New(this, 'SuppressHandlerFn')
      .HandlesMessenger('Vault-Suppress');

  }
}
