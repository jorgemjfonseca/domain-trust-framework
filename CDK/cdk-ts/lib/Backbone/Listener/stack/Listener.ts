import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { STACK } from '../../../Common/STACK/STACK';
import { Domain } from '../../../Behaviours/Domain/stack/Domain';
import { Publisher } from '../../../Behaviours/Publisher/stack/Publisher';
import { Subscriber } from '../../../Behaviours/Subscriber/stack/Subscriber';


interface ListenerDependencies {
  domain: Domain,
  publisher: Publisher,
  subscriber: Subscriber,
}


//https://quip.com/FCSiAU7Eku0X/-Listener
export class Listener extends STACK {

  public static New(scope: Construct, deps: ListenerDependencies, props?: cdk.StackProps): Listener {
    const ret = new Listener(scope, props);
    ret.addDependency(deps.domain);
    ret.addDependency(deps.publisher);
    ret.addDependency(deps.subscriber);
    return ret;
  }


  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, Listener.name, props);

    this.SetUpPublisher();
    this.SetUpSubscriber();
  }


  private SetUpPublisher() {

    const subscribers = Publisher.GetSubscribers(this);

    LAMBDA
      .New(this, 'Publisher')
      .FiltersPublisher()
      .ReadsFromDynamoDB(subscribers, 'SUBSCRIBERS')
      .PublishesToMessenger();
  }


  private SetUpSubscriber() {

    const dedups = Subscriber.GetDedups(this);

    LAMBDA
      .New(this, 'Subscriber')
      .TriggeredByDynamoDB(dedups);
  }

}
