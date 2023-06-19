import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../../Common/LAMBDA/LAMBDA';
import { BUS } from '../../../../Common/BUS/BUS';
import { DYNAMO } from '../../../../Common/DYNAMO/DYNAMO';
import { SharedComms } from '../../../../Behaviours/SharedComms/stack/SharedComms';
import { STACK } from '../../../../Common/STACK/STACK';

// https://quip.com/IZapAfPZPnOD
export class ThingsActor extends STACK {


  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, ThingsActor.name, props);

    const bus = BUS.Import(this, SharedComms.BUS);

    const things = DYNAMO
      .New(this, 'Things');

    const privates = DYNAMO
      .New(this, 'Privates');
   
    LAMBDA
      .New(this, 'CreateHandlerFn')
      .SpeaksWithBus(bus, 'Things-Create')
      .WritesToDynamoDBs([ things, privates ]);

  }
}
