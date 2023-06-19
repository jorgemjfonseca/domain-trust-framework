import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../../Common/LAMBDA/LAMBDA';
import { BUS } from '../../../../Common/BUS/BUS';
import { DYNAMO } from '../../../../Common/DYNAMO/DYNAMO';
import { API } from '../../../../Common/API/API';
import { SharedComms } from '../../../../Behaviours/SharedComms/stack/SharedComms';
import { SyncApiBehaviour } from '../../../../Behaviours/SyncApi/stack/SyncApiBehaviour';
import { STACK } from '../../../../Common/STACK/STACK';

// https://quip.com/U97qAoGmSPAn
export class PrinterActor extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, PrinterActor.name, props);

    const bus = BUS.Import(this, SharedComms.BUS);
    const router = API.Import(this, SyncApiBehaviour.ROUTER);

    const orders = DYNAMO
      .New(this, 'Orders');

    const locators = DYNAMO
      .New(this, 'Locators');

    LAMBDA
      .New(this, 'DetailsHandlerFn')
      .AddApiMethod(router, 'Printer-Details')
      .ReadsFromDynamoDB(locators);

    LAMBDA
      .New(this, 'GrabHandlerFn')
      .AddApiMethod(router, 'Printer-Grab')
      .WritesToDynamoDB(locators);

    LAMBDA
      .New(this, 'OrderHandlerFn')
      .SpeaksWithBus(bus, 'Printer-Order')
      .WritesToDynamoDB(orders);


  }
}
