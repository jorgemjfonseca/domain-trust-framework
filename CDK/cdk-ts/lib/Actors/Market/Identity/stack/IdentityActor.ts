import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../../Common/DYNAMO/DYNAMO';
import { STACK } from '../../../../Common/STACK/STACK';

// https://quip.com/f0BTAeva6BTE/-Identity
export class IdentityActor extends STACK {
  
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, IdentityActor.name, props);

    const otps = DYNAMO
      .New(this, 'OTPs');

    LAMBDA
      .New(this, 'ConfirmEmailHandlerFn')
      .WritesToDynamoDB(otps)
      .HandlesMessenger('Identity-ConfirmEmail');

    LAMBDA
      .New(this, 'ConfirmPhoneHandlerFn')
      .WritesToDynamoDB(otps)
      .HandlesMessenger('Identity-ConfirmPhone');

  }
}
