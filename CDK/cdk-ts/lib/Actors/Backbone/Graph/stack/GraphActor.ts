import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../../Common/LAMBDA/LAMBDA';
import { BUS } from '../../../../Common/BUS/BUS';
import { DYNAMO } from '../../../../Common/DYNAMO/DYNAMO';
import { API } from '../../../../Common/API/API';
import { NEPTUNE } from '../../../../Common/NEPTUNE/NEPTUNE';
import { SyncApiBehaviour } from '../../../../Behaviours/SyncApi/stack/SyncApiBehaviour';
import { SharedComms } from '../../../../Behaviours/SharedComms/stack/SharedComms';
import { STACK } from '../../../../Common/STACK/STACK';

// https://quip.com/hgz4A3clvOes/-Graph
export class GraphActor extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, GraphActor.name, props);

    const bus = BUS
      .Import(this, SharedComms.BUS);

    const routerApi = API
      .Import(this, SyncApiBehaviour.ROUTER);

    const neptune = NEPTUNE
      .New(this, 'Neptune');

    const domainsTable = DYNAMO
      .New(this, 'Domains', { stream: true });

    LAMBDA
      .New(this, 'ConsumeHandlerFn')
      .SpeaksWithBus(bus, 'Graph-Consume')
      .WritesToDynamoDB(domainsTable)
      .WritesToNeptune(neptune);

    LAMBDA
      .New(this, 'TrustedHandlerFn')
      .AddApiMethod(routerApi, 'Graph-Trusted')
      .ReadsFromDynamoDB(domainsTable)
      .ReadsFromNeptune(neptune);

    LAMBDA
      .New(this, 'TrustsHandlerFn')
      .AddApiMethod(routerApi, 'Graph-Trusts')
      .ReadsFromDynamoDB(domainsTable)
      .ReadsFromNeptune(neptune);

    LAMBDA
      .New(this, 'IdentityHandlerFn')
      .AddApiMethod(routerApi, 'Graph-Identity')
      .ReadsFromDynamoDB(domainsTable);

    LAMBDA
      .New(this, 'QueryableHandlerFn')
      .AddApiMethod(routerApi, 'Graph-Queryable')
      .ReadsFromDynamoDB(domainsTable)
      .ReadsFromNeptune(neptune);      

    LAMBDA
      .New(this, 'TranslateHandlerFn')
      .AddApiMethod(routerApi, 'Graph-Translate')
      .ReadsFromDynamoDB(domainsTable);

    LAMBDA
      .New(this, 'PublicKeyHandlerFn')
      .AddApiMethod(routerApi, 'Graph-PublicKey')
      .ReadsFromDynamoDB(domainsTable);

    LAMBDA
      .New(this, 'SchemaHandlerFn')
      .AddApiMethod(routerApi, 'Graph-Schema')
      .ReadsFromDynamoDB(domainsTable);      

    LAMBDA
      .New(this, 'PublisherFn')
      .TriggeredByDynamoDB(domainsTable)
      .PublishesToBus(bus);

  }
}
