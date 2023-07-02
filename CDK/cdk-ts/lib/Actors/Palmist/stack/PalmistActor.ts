import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { STACK } from '../../../Common/STACK/STACK';

// https://quip.com/YYLUAcmsT3R7
export class PalmistActor extends STACK {
  
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, PalmistActor.name, props);

    const devices = DYNAMO
      .New(this, 'Devices');

    const disclosures = DYNAMO
      .New(this, 'Disclosures');

    const delegates = DYNAMO
      .New(this, 'Delegates');

    LAMBDA
      .New(this, 'RegisterHandlerFn')
      .WritesToDynamoDB(devices, 'DEVICES')
      .HandlesMessenger('Register@Palmist');

    LAMBDA
      .New(this, 'DisclosedHandlerFn')
      .WritesToDynamoDB(devices, 'DEVICES')
      .WritesToDynamoDB(disclosures, 'DISCLOSURES')
      .HandlesSyncApi('Disclosed@Palmist');

    LAMBDA
      .New(this, 'MatchHandlerFn')
      .WritesToDynamoDB(devices, 'DEVICES')
      .WritesToDynamoDB(delegates, 'DELEGATES')
      .HandlesSyncApi('Match@Palmist');

    LAMBDA
      .New(this, 'SearchHandlerFn')
      .WritesToDynamoDB(devices, 'DEVICES')
      .HandlesMessenger('Search@Palmist');

    LAMBDA
      .New(this, 'DelegateHandlerFn')
      .WritesToDynamoDB(devices, 'DEVICES')
      .WritesToDynamoDB(delegates, 'DELEGATES')
      .HandlesMessenger('Delegate@Palmist');

    LAMBDA
      .New(this, 'SuppressedHandlerFn')
      .WritesToDynamoDB(devices, 'DEVICES')
      .HandlesMessenger('Suppressed@Palmist');

  }
}
