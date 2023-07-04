import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { STACK } from '../../../Common/STACK/STACK';
import { SyncApi } from '../../SyncApi/stack/SyncApi';
import { Messenger } from '../../Messenger/stack/Messenger';

export interface SubscriberDependencies {
  syncApi: SyncApi,
  messenger: Messenger
}

// 👉 https://quip.com/9ab7AO56kkxY/-Subscriber
export class Subscriber extends STACK {

  public static New(scope: Construct, deps: SubscriberDependencies, props?: cdk.StackProps) {
    const ret = new Subscriber(scope, props)
    ret.addDependency(deps.syncApi);
    ret.addDependency(deps.messenger);
    return ret;
  }

  private static readonly DEDUPS = 'Deduplication';
  public static GetDedups(scope: STACK) {
    return DYNAMO.Import(scope, Subscriber.DEDUPS);
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, Subscriber.name, { 
      description: 'Subscriber behaviour.',
      ...props
    });

    const dedups = DYNAMO
      .New(this, Subscriber.DEDUPS, {
        ttl: true,
        stream: true
      })
      .Export(Subscriber.DEDUPS);

    LAMBDA
      .New(this, "Confirm")
      .HandlesMessenger('Confirm@Subscriber');

    LAMBDA
      .New(this, "Updated")
      .HandlesMessenger('Updated@Subscriber')
      .WritesToDynamoDB(dedups, 'DEDUPS');

    LAMBDA
      .New(this, "Consume")
      .HandlesMessenger('Consume@Subscriber')
      .WritesToDynamoDB(dedups, 'DEDUPS');

  }
}
