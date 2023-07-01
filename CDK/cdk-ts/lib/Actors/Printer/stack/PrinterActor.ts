import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { STACK } from '../../../Common/STACK/STACK';

// https://quip.com/U97qAoGmSPAn
export class PrinterActor extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, PrinterActor.name, props);

    const orders = DYNAMO
      .New(this, 'Orders');

    const locators = DYNAMO
      .New(this, 'Locators');

    LAMBDA
      .New(this, 'DetailsHandlerFn')
      .ReadsFromDynamoDB(locators, 'LOCATORS')
      .HandlesSyncApi('Printer-Details');

    LAMBDA
      .New(this, 'GrabHandlerFn')
      .WritesToDynamoDB(locators, 'LOCATORS')
      .HandlesSyncApi('Printer-Grab');

    LAMBDA
      .New(this, 'OrderHandlerFn')
      .WritesToDynamoDB(orders, 'ORDERS')
      .HandlesMessenger('Printer-Order');

  }
}
