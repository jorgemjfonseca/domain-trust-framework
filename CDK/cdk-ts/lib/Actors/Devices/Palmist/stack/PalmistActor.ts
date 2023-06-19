import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../../Common/LAMBDA/LAMBDA';
import { BUS } from '../../../../Common/BUS/BUS';
import { DYNAMO } from '../../../../Common/DYNAMO/DYNAMO';
import { API } from '../../../../Common/API/API';
import { SharedComms } from '../../../../Behaviours/SharedComms/stack/SharedComms';
import { SyncApiBehaviour } from '../../../../Behaviours/SyncApi/stack/SyncApiBehaviour';
import { STACK } from '../../../../Common/STACK/STACK';

// https://quip.com/YYLUAcmsT3R7
export class PalmistActor extends STACK {
  
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, PalmistActor.name, props);

    const bus = BUS
      .Import(this, SharedComms.BUS);

    const routerApi = API
      .Import(this, SyncApiBehaviour.ROUTER);

    const devices = DYNAMO
      .New(this, 'Devices');

    const disclosures = DYNAMO
      .New(this, 'Disclosures');

    const delegates = DYNAMO
      .New(this, 'Delegates');

    LAMBDA
      .New(this, 'RegisterHandlerFn')
      .SpeaksWithBus(bus, 'Palmist-Register')
      .WritesToDynamoDBs([ devices ]);

    LAMBDA
      .New(this, 'DisclosedHandlerFn')
      .AddApiMethod(routerApi, 'Palmist-Disclosed')
      .WritesToDynamoDBs([ devices, disclosures ]);

    LAMBDA
      .New(this, 'MatchHandlerFn')
      .AddApiMethod(routerApi, 'Palmist-Match')
      .WritesToDynamoDBs([ devices, delegates ]);

    LAMBDA
      .New(this, 'SearchHandlerFn')
      .SpeaksWithBus(bus, 'Palmist-Search')
      .WritesToDynamoDBs([ devices ]);

    LAMBDA
      .New(this, 'DelegateHandlerFn')
      .SpeaksWithBus(bus, 'Palmist-Delegate')
      .WritesToDynamoDBs([ devices, delegates ]);

    LAMBDA
      .New(this, 'SuppressedHandlerFn')
      .SpeaksWithBus(bus, 'Palmist-Suppressed')
      .WritesToDynamoDBs([ devices ]);

  }
}
