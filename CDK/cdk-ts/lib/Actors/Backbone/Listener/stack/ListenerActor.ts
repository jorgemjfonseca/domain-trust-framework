import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../../Common/LAMBDA/LAMBDA';
import { STACK } from '../../../../Common/STACK/STACK';

//https://quip.com/FCSiAU7Eku0X/-Listener
export class ListenerActor extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, ListenerActor.name, props);

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
