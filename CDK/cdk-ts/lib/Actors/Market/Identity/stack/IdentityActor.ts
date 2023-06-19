import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../../Common/LAMBDA/LAMBDA';
import { BUS } from '../../../../Common/BUS/BUS';
import { DYNAMO } from '../../../../Common/DYNAMO/DYNAMO';
import { SharedComms } from '../../../../Behaviours/SharedComms/stack/SharedComms';
import { STACK } from '../../../../Common/STACK/STACK';

// https://quip.com/f0BTAeva6BTE/-Identity
export class IdentityActor extends STACK {
  
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, IdentityActor.name, props);

    const bus = BUS.Import(this, SharedComms.BUS);

    const otps = DYNAMO
      .New(this, 'OTPs');

    LAMBDA
      .New(this, 'ConfirmEmailHandlerFn')
      .SpeaksWithBus(bus, 'Identity-ConfirmEmail')
      .WritesToDynamoDB(otps);

    LAMBDA
      .New(this, 'ConfirmPhoneHandlerFn')
      .SpeaksWithBus(bus, 'Identity-ConfirmPhone')
      .WritesToDynamoDB(otps);

  }
}
