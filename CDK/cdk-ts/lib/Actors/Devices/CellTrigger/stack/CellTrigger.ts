import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../../Common/LAMBDA/LAMBDA';
import { BUS } from '../../../../Common/BUS/BUS';
import { DYNAMO } from '../../../../Common/DYNAMO/DYNAMO';
import { API } from '../../../../Common/API/API';
import { SharedComms } from '../../../../Behaviours/SharedComms/stack/SharedComms';
import { STACK } from '../../../../Common/STACK/STACK';

// https://quip.com/UbZGA7PKb7ar/-Cell-Trigger
export class CellTriggerActor extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, CellTriggerActor.name, props);

    const bus = BUS
      .Import(this, SharedComms.BUS);

    const orders = DYNAMO
      .New(this, 'Orders');

    const devices = DYNAMO
      .New(this, 'Devices');

    LAMBDA
      .New(this, 'TriggerHandlerFn')
      .SpeaksWithBus(bus, 'CellTrigger-Trigger')
      .WritesToDynamoDB(devices);

    LAMBDA
      .New(this, 'OrderHandlerFn')
      .SpeaksWithBus(bus, 'CellTrigger-Updated')
      .WritesToDynamoDBs([ orders, devices ]);
      
  }
}
