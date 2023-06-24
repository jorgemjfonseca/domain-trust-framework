import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../../Common/DYNAMO/DYNAMO';
import { NEPTUNE } from '../../../../Common/NEPTUNE/NEPTUNE';
import { STACK } from '../../../../Common/STACK/STACK';

// https://quip.com/hgz4A3clvOes/-Graph
export class Graph extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, Graph.name, props);

    const domainsTable = DYNAMO
      .New(this, 'Domains', { stream: true });

    LAMBDA
      .New(this, 'ConsumeHandlerFn')
      .WritesToDynamoDB(domainsTable)
      //.WritesToNeptune(neptune)
      .HandlesMessenger('Graph-Consume');

    LAMBDA
      .New(this, 'TrustedHandlerFn')
      .ReadsFromDynamoDB(domainsTable)
      //.ReadsFromNeptune(neptune)
      .HandlesSyncApi('Graph-Trusted');

    LAMBDA
      .New(this, 'TrustsHandlerFn')
      .ReadsFromDynamoDB(domainsTable)
      //.ReadsFromNeptune(neptune)
      .HandlesSyncApi('Graph-Trusts');

    LAMBDA
      .New(this, 'IdentityHandlerFn')
      .ReadsFromDynamoDB(domainsTable)
      .HandlesSyncApi('Graph-Identity');

    LAMBDA
      .New(this, 'QueryableHandlerFn')
      .ReadsFromDynamoDB(domainsTable)
      //.ReadsFromNeptune(neptune)
      .HandlesSyncApi('Graph-Queryable');      

    LAMBDA
      .New(this, 'TranslateHandlerFn')
      .ReadsFromDynamoDB(domainsTable)
      .HandlesSyncApi('Graph-Translate');

    LAMBDA
      .New(this, 'PublicKeyHandlerFn')
      .ReadsFromDynamoDB(domainsTable)
      .HandlesSyncApi('Graph-PublicKey');

    LAMBDA
      .New(this, 'SchemaHandlerFn')
      .ReadsFromDynamoDB(domainsTable)
      .HandlesSyncApi('Graph-Schema');      

    LAMBDA
      .New(this, 'PublisherFn')
      .TriggeredByDynamoDB(domainsTable)
      .PublishesToMessenger();

  }
}
