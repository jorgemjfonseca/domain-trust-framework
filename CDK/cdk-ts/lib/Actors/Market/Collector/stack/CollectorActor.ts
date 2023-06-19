import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../../Common/LAMBDA/LAMBDA';
import { BUS } from '../../../../Common/BUS/BUS';
import { DYNAMO } from '../../../../Common/DYNAMO/DYNAMO';
import { API } from '../../../../Common/API/API';
import { SharedComms } from '../../../../Behaviours/SharedComms/stack/SharedComms';
import { SyncApiBehaviour } from '../../../../Behaviours/SyncApi/stack/SyncApiBehaviour';
import { STACK } from '../../../../Common/STACK/STACK';

// https://quip.com/TkhkAIHSg8Pp/-Collector
export class CollectorActor extends STACK {

  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, CollectorActor.name, props);

    const bus = BUS
      .Import(this, SharedComms.BUS);

    const router = API
      .Import(this, SyncApiBehaviour.ROUTER);

    const collections = DYNAMO
      .New(this, 'Collections');
      
    const refunds = DYNAMO
      .New(this, 'Refunds');

    LAMBDA
      .New(this, 'CollectHandlerFn')
      .SpeaksWithBus(bus, 'Collector-Collect')
      .WritesToDynamoDB(collections);

    LAMBDA
      .New(this, 'RefundHandlerFn')
      .SpeaksWithBus(bus, 'Collector-Refund')
      .WritesToDynamoDB(refunds);

    LAMBDA
      .New(this, 'UnsubscribeHandlerFn')
      .AddApiMethod(router, 'Collector-Unsubscribe');

  }
}
