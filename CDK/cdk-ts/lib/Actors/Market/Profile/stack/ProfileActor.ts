import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../../Common/DYNAMO/DYNAMO';
import { VaultActor } from '../../Vault/stack/VaultActor';
import { STACK } from '../../../../Common/STACK/STACK';

// https://quip.com/SEI9ASIzc2C5/-Profile
export class ProfileActor extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, ProfileActor.name, props);

    const userData = DYNAMO
      .New(this, 'UserData');

    LAMBDA
      .Import(this, VaultActor.DISCLOSE_FN)
      .ReadsFromDynamoDB(userData, 'USERDATA');

  }
}
