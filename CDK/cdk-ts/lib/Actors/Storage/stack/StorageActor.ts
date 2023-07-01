import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { STACK } from '../../../Common/STACK/STACK';

// https://quip.com/8OSLACqhObc0/-Storage
export class StorageActor extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, StorageActor.name, props);
  
    const things = DYNAMO
      .New(this, 'Things');

    const files = DYNAMO
      .New(this, 'Files');

    LAMBDA
      .New(this, 'CreateHandlerFn')
      .WritesToDynamoDB(things, 'THINGS')
      .WritesToDynamoDB(files, 'FILES')
      .HandlesMessenger('Storage-Create');

  }
}
