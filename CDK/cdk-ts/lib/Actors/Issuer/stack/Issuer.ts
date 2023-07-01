import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { STACK } from '../../../Common/STACK/STACK';

// https://quip.com/a167Ak79FKlt/-Issuer
export class Issuer extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, Issuer.name, props);

    const credentials = DYNAMO
      .New(this, 'Credentials');

    LAMBDA
      .New(this, 'Download')
      .ReadsFromDynamoDB(credentials, 'CREDENTIALS')
      .HandlesSyncApi('Issuer-Download');

    LAMBDA
      .New(this, 'Status')
      .ReadsFromDynamoDB(credentials, 'CREDENTIALS')
      .HandlesMessenger('Issuer-Status');

  }
}
