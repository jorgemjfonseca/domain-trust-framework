import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/Lambda/Lambda';
import { BUS } from '../../../Common/EventBus/EventBus';
import { DYNAMO } from '../../../Common/DynamoDB/DynamoDB';
import { API } from '../../../Common/ApiGW/Api';

//https://quip.com/FCSiAU7Eku0X/-Listener
export class ActorListener extends cdk.Stack {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, ActorListener.name, props);

    const bus = BUS.Import(this, 'DomainBus');

    LAMBDA
      .New(this, 'SubscribeHandlerFn')
      .TriggeredByBus(bus, ['DTFW'], ['Subscribe'])
      .PublishesToBus(bus);

    LAMBDA
      .New(this, 'UpdatedHandlerFn')
      .TriggeredByBus(bus, ['DTFW'], ['Updated'])
      .PublishesToBus(bus);

    LAMBDA
      .New(this, 'ConsumeHandlerFn')
      .TriggeredByBus(bus, ['DTFW'], ['Consume'])
      .PublishesToBus(bus);

    LAMBDA
      .New(this, 'PublisherFn')
      .TriggeredByBus(bus, ['DTFW'], ['Publisher'])
      .PublishesToBus(bus);

  }
}
