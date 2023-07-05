import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';


/** 👉 https://quip.com/rKzMApUS5QIi#WTIABAsxxkW */
export class BrokerShare extends STACK {

  public static New (scope: Construct, props?: cdk.StackProps): BrokerShare {
    return new BrokerShare(scope, props);
  }

  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, BrokerShare.name, props);

    const queries = DYNAMO.New(this, 'Queries')

    LAMBDA
      .New(this, 'Query')
      .WritesToDynamoDB(queries, 'QUERIES')
      .HandlesMessenger('Query@Broker')

  }

}
