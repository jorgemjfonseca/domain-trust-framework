import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { STACK } from '../../../Common/STACK/STACK';

// https://quip.com/UbZGA7PKb7ar/-Cell-Trigger
export class CellTriggerActor extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, CellTriggerActor.name, props);

    const orders = DYNAMO
      .New(this, 'Orders');

    const devices = DYNAMO
      .New(this, 'Devices');

    LAMBDA
      .New(this, 'Trigger')
      .WritesToDynamoDB(devices, 'DEVICES')
      .HandlesMessenger('Trigger@CellTrigger');

    LAMBDA
      .New(this, 'Order')
      .WritesToDynamoDB(orders, 'ORDERS')
      .WritesToDynamoDB(devices, 'DEVICES')
      .HandlesMessenger('Updated@CellTrigger');
      
  }
}
