import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { NEPTUNE } from '../../../Common/NEPTUNE/NEPTUNE';
import { STACK } from '../../../Common/STACK/STACK';
import { Domain } from '../../../Behaviours/Domain/stack/Domain';
import { Subscriber } from '../../../Behaviours/Subscriber/stack/Subscriber';
import { GraphDB } from '../../GraphDB/stack/GraphDB';
import { Publisher } from '../../../Behaviours/Publisher/stack/Publisher';


export interface GraphDependencies {
  domain: Domain,
  subscriber: Subscriber,
  publisher: Publisher,
  graphDB: GraphDB
}


// 👉 https://quip.com/hgz4A3clvOes/-Graph
export class Graph extends STACK {

  public static New(scope: Construct, deps: GraphDependencies, props?: cdk.StackProps) {
    const ret = new Graph(scope, props);
    ret.addDependency(deps.domain);
    ret.addDependency(deps.subscriber);
    ret.addDependency(deps.publisher);
    //ret.addDependency(deps.graphDB);
    return ret;
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, Graph.name, { 
      description: 'Graph backbone actor.',
      ...props
    });

    const domainsTable = DYNAMO
      .New(this, 'Domains', { stream: true });

    const codesTable = DYNAMO
      .New(this, 'Codes');

    const dedups = Subscriber.GetDedups(this);

    // 🐌 https://quip.com/hgz4A3clvOes#temp:C:bDAeaf662df90ec442284b7aaef9
    LAMBDA
      .New(this, 'Subscriber')
      .TriggeredByDynamoDB(dedups)
      .WritesToDynamoDB(domainsTable, 'DOMAINS')
      .WritesToDynamoDB(codesTable, 'CODES');
      //.WritesToNeptune(neptune);

    // 🚀 https://quip.com/hgz4A3clvOes#temp:C:bDA0807933d618043e6b1873dc74
    LAMBDA
      .New(this, 'Trusted')
      .ReadsFromDynamoDB(domainsTable, 'DOMAINS')
      //.ReadsFromNeptune(neptune)
      .HandlesSyncApi('Trusted@Graph', { ignoreValidation: true });

    // 🚀 https://quip.com/hgz4A3clvOes#temp:C:bDA71b470c7a4c446e5b43adea7e
    LAMBDA
      .New(this, 'Trusts')
      .ReadsFromDynamoDB(domainsTable, 'DOMAINS')
      //.ReadsFromNeptune(neptune)
      .HandlesSyncApi('Trusts@Graph', { ignoreValidation: true });

    // 🚀 https://quip.com/hgz4A3clvOes#temp:C:bDAacb56742c6a342a8a3494587d
    LAMBDA
      .New(this, 'Identity', { yaml: true })
      .ReadsFromDynamoDB(domainsTable, 'DOMAINS')
      .HandlesSyncApi('Identity@Graph', { ignoreValidation: true });

    // 🚀 https://quip.com/hgz4A3clvOes#temp:C:bDA44399e7e0bfc4609a560d6c4a
    LAMBDA
      .New(this, 'Queryable')
      .ReadsFromDynamoDB(domainsTable, 'DOMAINS')
      //.ReadsFromNeptune(neptune)
      .HandlesSyncApi('Queryable@Graph', { ignoreValidation: true });

    // 🚀 https://quip.com/hgz4A3clvOes#temp:C:bDA9d34010d13574c2f95fe4de54
    LAMBDA
      .New(this, 'Translate')
      .ReadsFromDynamoDB(domainsTable, 'DOMAINS')
      .ReadsFromDynamoDB(codesTable, 'CODES')
      .HandlesSyncApi('Translate@Graph', { ignoreValidation: true });

    // 🚀 https://quip.com/hgz4A3clvOes#temp:C:bDAe17e4b66e30846a7b82ecce0c
    LAMBDA
      .New(this, 'PublicKey')
      .ReadsFromDynamoDB(domainsTable, 'DOMAINS')
      .HandlesSyncApi('PublicKey@Graph', { ignoreValidation: true });

    // 🚀 https://quip.com/hgz4A3clvOes#temp:C:bDAe24fd83cf9c244078a0f67f7f
    LAMBDA
      .New(this, 'Schema')
      .ReadsFromDynamoDB(domainsTable, 'DOMAINS')
      .ReadsFromDynamoDB(codesTable, 'CODES')
      .HandlesSyncApi('Schema@Graph', { ignoreValidation: true });    

  }
}
