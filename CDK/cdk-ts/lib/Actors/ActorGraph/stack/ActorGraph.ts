import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/Lambda/Lambda';
import { BUS } from '../../../Common/EventBus/EventBus';
import { DYNAMO } from '../../../Common/DynamoDB/DynamoDB';
import { API } from '../../../Common/ApiGW/Api';
import { NEPTUNE } from '../../../Common/Neptune/Neptune';

// https://quip.com/hgz4A3clvOes/-Graph
export class ActorGraph extends cdk.Stack {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, ActorGraph.name, props);

    const bus = BUS
      .Import(this, "DomainBus");

    const routerApi = API
      .Import(this, "SyncRouterApi");

    const neptune = NEPTUNE
      .New(this, 'Neptune');

    const domainsTable = DYNAMO
      .New(this, 'Domains', { stream: true });

    LAMBDA
      .New(this, 'SubscriberFn')
      .TriggeredByBus(bus, ['DTFW'], ['UPDATE'])
      .WritesToDynamoDB(domainsTable)
      .WritesToNeptune(neptune);

    LAMBDA
      .New(this, 'SyncApiFn')
      .WritesToDynamoDB(domainsTable)
      .WritesToNeptune(neptune)
      .AddApiMethod(routerApi, 'Query');

    LAMBDA
      .New(this, 'PublisherFn')
      .TriggeredByDynamoDB(domainsTable)
      .PublishesToBus(bus);

  }
}
