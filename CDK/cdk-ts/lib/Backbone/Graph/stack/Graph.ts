import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { NEPTUNE } from '../../../Common/NEPTUNE/NEPTUNE';
import { STACK } from '../../../Common/STACK/STACK';
import { Domain } from '../../../Behaviours/Domain/stack/Domain';
import { Subscriber } from '../../../Behaviours/Subscriber/stack/Subscriber';
import { GraphDB } from '../../GraphDB/stack/GraphDB';


export interface GraphDependencies {
  domain: Domain,
  subscriber: Subscriber,
  graphDB: GraphDB
}


// 👉 https://quip.com/hgz4A3clvOes/-Graph
export class Graph extends STACK {

  public static New(scope: Construct, deps: GraphDependencies, props?: cdk.StackProps) {
    const ret = new Graph(scope, props);
    ret.addDependency(deps.domain);
    ret.addDependency(deps.subscriber);
    //ret.addDependency(deps.graphDB);
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
      .WritesToDynamoDB(codesTable, 'CODES')
      //.WritesToNeptune(neptune)
      .HandlesMessenger('Graph-Consume');

    LAMBDA
      .New(this, 'Trusted')
      .ReadsFromDynamoDB(domainsTable, 'DOMAINS')
      //.ReadsFromNeptune(neptune)
      .HandlesSyncApi('Graph-Trusted', { ignoreValidation: true });

    LAMBDA
      .New(this, 'Trusts')
      .ReadsFromDynamoDB(domainsTable, 'DOMAINS')
      //.ReadsFromNeptune(neptune)
      .HandlesSyncApi('Graph-Trusts', { ignoreValidation: true });

    LAMBDA
      .New(this, 'Identity')
      .ReadsFromDynamoDB(domainsTable, 'DOMAINS')
      .HandlesSyncApi('Graph-Identity', { ignoreValidation: true });

    LAMBDA
      .New(this, 'Queryable')
      .ReadsFromDynamoDB(domainsTable, 'DOMAINS')
      //.ReadsFromNeptune(neptune)
      .HandlesSyncApi('Graph-Queryable', { ignoreValidation: true });

    LAMBDA
      .New(this, 'Translate')
      .ReadsFromDynamoDB(domainsTable, 'DOMAINS')
      .ReadsFromDynamoDB(codesTable, 'CODES')
      .HandlesSyncApi('Graph-Translate', { ignoreValidation: true });

    LAMBDA
      .New(this, 'PublicKey')
      .ReadsFromDynamoDB(domainsTable, 'DOMAINS')
      .HandlesSyncApi('Graph-PublicKey', { ignoreValidation: true });

    LAMBDA
      .New(this, 'Schema')
      .ReadsFromDynamoDB(domainsTable, 'DOMAINS')
      .ReadsFromDynamoDB(codesTable, 'CODES')
      .HandlesSyncApi('Graph-Schema', { ignoreValidation: true });      

    LAMBDA
      .New(this, 'Publisher')
      .TriggeredByDynamoDB(domainsTable)
      .PublishesToMessenger();

  }
}
