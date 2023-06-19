import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../../Common/LAMBDA/LAMBDA';
import { BUS } from '../../../../Common/BUS/BUS';
import { DYNAMO } from '../../../../Common/DYNAMO/DYNAMO';
import { API } from '../../../../Common/API/API';
import { SharedComms } from '../../../../Behaviours/SharedComms/stack/SharedComms';
import { SyncApiBehaviour } from '../../../../Behaviours/SyncApi/stack/SyncApiBehaviour';
import { STACK } from '../../../../Common/STACK/STACK';

// https://quip.com/EzmaAjGwmvRq/-Payer
export class PayerActor extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, PayerActor.name, props);

    const bus = BUS.Import(this, SharedComms.BUS);
    const router = API.Import(this, SyncApiBehaviour.ROUTER);

    const endorsements = DYNAMO
      .New(this, 'Endorsements');

    const collections = DYNAMO
      .New(this, 'Collections');

    LAMBDA
      .New(this, 'EndorseHandlerFn')
      .SpeaksWithBus(bus, 'Payer-Endorse')
      .ReadsFromDynamoDB(endorsements);

    LAMBDA
      .New(this, 'CollectHandlerFn')
      .SpeaksWithBus(bus, 'Payer-Collect')
      .ReadsFromDynamoDB(collections);

  }
}
