import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../Common/Lambda/Lambda';
import { BUS } from '../../Common/EventBus/EventBus';
import { DYNAMO } from '../../Common/DynamoDB/DynamoDB';

export class DomainPublisher extends cdk.Stack {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, DomainPublisher.name, props);

    const bus = BUS.Import(this, "DomainBus");

    const senderFn = LAMBDA
      .New(this, "PublisherFn")
      .TriggeredByBus(bus, ['DTFW'], ['PUBLISH'])
      .PublishesToBus(bus)
      .WritesToDynamoDB(DYNAMO.New(this, "Subscribers"))
      .WritesToDynamoDB(DYNAMO.New(this, "Updates"));

  }
}
