import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { NEPTUNE } from '../../../Common/NEPTUNE/NEPTUNE';
import { STACK } from '../../../Common/STACK/STACK';
import { Domain } from '../../../Behaviours/Domain/stack/Domain';
import { Subscriber } from '../../../Behaviours/Subscriber/stack/Subscriber';


export interface GraphDependencies {
  domain: Domain,
  subscriber: Subscriber
}


// 👉 https://quip.com/hgz4A3clvOes/-Graph
export class Graph extends STACK {

  public static New(scope: Construct, deps: GraphDependencies, props?: cdk.StackProps) {
    const ret = new Graph(scope, props);
    ret.addDependency(deps.domain);
    ret.addDependency(deps.subscriber);
    return ret;
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, Graph.name, props);

    const domainsTable = DYNAMO
      .New(this, 'Domains', { stream: true });

    const codesTable = DYNAMO
      .New(this, 'Codes');

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
