import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../../Common/LAMBDA/LAMBDA';
import { BUS } from '../../../../Common/BUS/BUS';
import { DYNAMO } from '../../../../Common/DYNAMO/DYNAMO';
import { SharedComms } from '../../../../Behaviours/SharedComms/stack/SharedComms';
import { STACK } from '../../../../Common/STACK/STACK';

// https://quip.com/IZapAfPZPnOD
export class VaultActor extends STACK {

  public static readonly DISCLOSE_FN = 'Vault-DiscloseHandlerFn';
  public static readonly BINDS = 'Vault-BindsTable';
  public static readonly WALLETS = 'Vault-WalletsTable';


  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, VaultActor.name, props);

    const bus = BUS.Import(this, SharedComms.BUS);

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
      .SpeaksWithBus(bus, 'Vault-Bind')
      .WritesToDynamoDB(binds);

    LAMBDA
      .New(this, 'DiscloseHandlerFn')
      .SpeaksWithBus(bus, 'Vault-Disclose')
      .WritesToDynamoDB(disclosures)
      .Export(VaultActor.DISCLOSE_FN);

    LAMBDA
      .New(this, 'ContinueHandlerFn')
      .SpeaksWithBus(bus, 'Vault-Continue');

    LAMBDA
      .New(this, 'UnbindHandlerFn')
      .SpeaksWithBus(bus, 'Vault-Unbind');

    LAMBDA
      .New(this, 'SuppressHandlerFn')
      .SpeaksWithBus(bus, 'Vault-Suppress');

  }
}
