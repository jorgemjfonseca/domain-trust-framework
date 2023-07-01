import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { NEPTUNE } from '../../../Common/NEPTUNE/NEPTUNE';
import { STACK } from '../../../Common/STACK/STACK';

// https://quip.com/hgz4A3clvOes/-Graph
export class Graph extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, Graph.name, props);

    const domainsTable = DYNAMO
      .New(this, 'Domains', { stream: true });

    LAMBDA
      .New(this, 'Consume')
      .WritesToDynamoDB(domainsTable, 'DOMAINS')
      //.WritesToNeptune(neptune)
      .HandlesMessenger('Graph-Consume');

    LAMBDA
      .New(this, 'Trusted')
      .ReadsFromDynamoDB(domainsTable, 'DOMAINS')
      //.ReadsFromNeptune(neptune)
      .HandlesSyncApi('Graph-Trusted');

    LAMBDA
      .New(this, 'Trusts')
      .ReadsFromDynamoDB(domainsTable, 'DOMAINS')
      //.ReadsFromNeptune(neptune)
      .HandlesSyncApi('Graph-Trusts');

    LAMBDA
      .New(this, 'Identity')
      .ReadsFromDynamoDB(domainsTable, 'DOMAINS')
      .HandlesSyncApi('Graph-Identity');

    LAMBDA
      .New(this, 'Queryable')
      .ReadsFromDynamoDB(domainsTable, 'DOMAINS')
      //.ReadsFromNeptune(neptune)
      .HandlesSyncApi('Graph-Queryable');      

    LAMBDA
      .New(this, 'Translate')
      .ReadsFromDynamoDB(domainsTable, 'DOMAINS')
      .HandlesSyncApi('Graph-Translate');

    LAMBDA
      .New(this, 'PublicKey')
      .ReadsFromDynamoDB(domainsTable, 'DOMAINS')
      .HandlesSyncApi('Graph-PublicKey');

    LAMBDA
      .New(this, 'Schema')
      .ReadsFromDynamoDB(domainsTable, 'DOMAINS')
      .HandlesSyncApi('Graph-Schema');      

    LAMBDA
      .New(this, 'Publisher')
      .TriggeredByDynamoDB(domainsTable)
      .PublishesToMessenger();

  }
}
