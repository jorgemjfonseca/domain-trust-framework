import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/Lambda/Lambda';
import { BUS } from '../../../Common/EventBus/EventBus';
import { DYNAMO } from '../../../Common/DynamoDB/DynamoDB';

// https://quip.com/s9oCAO3UR38A/-Host
export class DomainHost extends cdk.Stack {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, DomainHost.name, props);

    const bus = BUS.Import(this, "DomainBus");

    const senderFn = LAMBDA
      .New(this, "HandlerFn")
      .TriggeredByBus(bus, ['DTFW'], ['SESSION'])
      .PublishesToBus(bus)
      .WritesToDynamoDB(DYNAMO.New(this, "Sessions"));

  }
}
