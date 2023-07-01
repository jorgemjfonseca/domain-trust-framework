import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { STACK } from '../../../Common/STACK/STACK';

// https://quip.com/IZapAfPZPnOD
export class ThingsActor extends STACK {


  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, ThingsActor.name, props);

    const things = DYNAMO
      .New(this, 'Things');

    const privates = DYNAMO
      .New(this, 'Privates');
   
    LAMBDA
      .New(this, 'CreateHandlerFn')
      .WritesToDynamoDB(things, 'THINGS')
      .WritesToDynamoDB(privates, 'PRIVATES')
      .HandlesMessenger('Things-Create');

  }
}
