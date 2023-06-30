import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../../Common/DYNAMO/DYNAMO';
import { VaultActor } from '../../Vault/stack/VaultActor';
import { STACK } from '../../../../Common/STACK/STACK';

// https://quip.com/UbokAEferibV/-Consumer
export class ConsumerActor extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, ConsumerActor.name, props);

    const binds = DYNAMO
      .Import(this, VaultActor.BINDS);

    LAMBDA
      .New(this, 'UploadHandlerFn')
      .ReadsFromDynamoDB(binds, 'BINDS')
      .HandlesMessenger('Consumer-Upload');

    LAMBDA
      .New(this, 'ConsumeHandlerFn')
      .HandlesMessenger('Consumer-Consume');

  }
}
