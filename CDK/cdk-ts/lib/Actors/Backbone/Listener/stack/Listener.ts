import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../../Common/LAMBDA/LAMBDA';
import { STACK } from '../../../../Common/STACK/STACK';
import { Domain } from '../../../../Behaviours/Domain/stack/Domain';
import { Publisher } from '../../../../Behaviours/Publisher/stack/Publisher';

interface ListenerDependencies {
  domain: Domain,
  publisher: Publisher
}

//https://quip.com/FCSiAU7Eku0X/-Listener
export class Listener extends STACK {

  public static New(scope: Construct, deps: ListenerDependencies, props?: cdk.StackProps): Listener {
    const ret = new Listener(scope, props);
    ret.addDependency(deps.domain);
    ret.addDependency(deps.publisher);
    return ret;
  }


  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, Listener.name, props);

    LAMBDA
      .New(this, 'SubscribeHandlerFn')
      .HandlesMessenger('Listener-Subscribe');

    LAMBDA
      .New(this, 'UpdatedHandlerFn')
      .HandlesMessenger('Listener-Updated');

    LAMBDA
      .New(this, 'ConsumeHandlerFn')
      .HandlesMessenger('Listener-Consume');

    LAMBDA
      .New(this, 'PublisherFn')
      .HandlesMessenger('Listener-Publisher');

  }
}
