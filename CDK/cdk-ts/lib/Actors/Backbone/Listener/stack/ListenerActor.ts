import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../../Common/LAMBDA/LAMBDA';
import { BUS } from '../../../../Common/BUS/BUS';
import { SharedComms } from '../../../../Behaviours/SharedComms/stack/SharedComms';
import { STACK } from '../../../../Common/STACK/STACK';

//https://quip.com/FCSiAU7Eku0X/-Listener
export class ListenerActor extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, ListenerActor.name, props);

    const bus = BUS.Import(this, SharedComms.BUS);

    LAMBDA
      .New(this, 'SubscribeHandlerFn')
      .SpeaksWithBus(bus, 'Listener-Subscribe');

    LAMBDA
      .New(this, 'UpdatedHandlerFn')
      .SpeaksWithBus(bus, 'Listener-Updated');

    LAMBDA
      .New(this, 'ConsumeHandlerFn')
      .SpeaksWithBus(bus, 'Listener-Consume');

    LAMBDA
      .New(this, 'PublisherFn')
      .SpeaksWithBus(bus, 'Listener-Publisher');

  }
}
