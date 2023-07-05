import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';


/** 👉 https://quip.com/sN8DACFLN9wM#AfTABAujlEx */
export class BrokerCredentials extends STACK {

  public static New(scope: Construct, props?: cdk.StackProps): BrokerCredentials {
    const ret = new BrokerCredentials(scope, props);
    return ret;
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, BrokerCredentials.name, props);

    const issuers = DYNAMO.New(this, 'Issuers')
    const credentials = DYNAMO.New(this, 'Credentials')

    LAMBDA
      .New(this, 'Issue')
      .WritesToDynamoDB(issuers, 'ISSUERS')
      .WritesToDynamoDB(credentials, 'CREDENTIALS')
      .HandlesMessenger('Issue@Broker');

    LAMBDA  
      .New(this, 'Revoke')
      .ReadsFromDynamoDB(issuers, 'ISSUERS')
      .WritesToDynamoDB(credentials, 'CREDENTIALS')
      .HandlesMessenger('Revoke@Broker');

    LAMBDA
      .New(this, 'Accepted')
      .ReadsFromDynamoDB(issuers, 'ISSUERS')
      .WritesToDynamoDB(credentials, 'CREDENTIALS')
      .HandlesMessenger('Accepted@Broker');

    LAMBDA
      .New(this, 'Credentials')
      .ReadsFromDynamoDB(issuers, 'ISSUERS')
      .ReadsFromDynamoDB(credentials, 'CREDENTIALS')
      .HandlesSyncApi('Credentials@Broker');

    LAMBDA
      .New(this, 'Remove')
      .WritesToDynamoDB(issuers, 'ISSUERS')
      .WritesToDynamoDB(credentials, 'CREDENTIALS')
      .HandlesMessenger('Remove@Broker');


  }
}
