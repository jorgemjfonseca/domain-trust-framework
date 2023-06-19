import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../../Common/LAMBDA/LAMBDA';
import { BUS } from '../../../../Common/BUS/BUS';
import { DYNAMO } from '../../../../Common/DYNAMO/DYNAMO';
import { API } from '../../../../Common/API/API';
import { SharedComms } from '../../../../Behaviours/SharedComms/stack/SharedComms';
import { SyncApiBehaviour } from '../../../../Behaviours/SyncApi/stack/SyncApiBehaviour';
import { STACK } from '../../../../Common/STACK/STACK';

// https://quip.com/3HanAwD0KfJg/-Wi-Fi
export class WiFiActor extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, WiFiActor.name, props);

    const bus = BUS.Import(this, SharedComms.BUS);

    const routerApi = API
      .Import(this, SyncApiBehaviour.ROUTER);
      
    LAMBDA
      .New(this, 'ConsumeHandlerFn')
      .AddApiMethod(routerApi, 'WiFi-Consume');
  }
}
