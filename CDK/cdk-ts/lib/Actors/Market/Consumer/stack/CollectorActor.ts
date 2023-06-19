import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../../Common/LAMBDA/LAMBDA';
import { BUS } from '../../../../Common/BUS/BUS';
import { DYNAMO } from '../../../../Common/DYNAMO/DYNAMO';
import { SharedComms } from '../../../../Behaviours/SharedComms/stack/SharedComms';
import { VaultActor } from '../../Vault/stack/VaultActor';
import { STACK } from '../../../../Common/STACK/STACK';

// https://quip.com/UbokAEferibV/-Consumer
export class ConsumerActor extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, ConsumerActor.name, props);

    const bus = BUS.Import(this, SharedComms.BUS);
    const binds = DYNAMO.Import(this, VaultActor.BINDS);

    LAMBDA
      .New(this, 'UploadHandlerFn')
      .TriggeredByBus(bus, 'Consumer-Upload')
      .PublishesToBus(bus)
      .ReadsFromDynamoDB(binds);

    LAMBDA
      .New(this, 'ConsumeHandlerFn')
      .TriggeredByBus(bus, 'Consumer-Consume')
      .PublishesToBus(bus);

  }
}
