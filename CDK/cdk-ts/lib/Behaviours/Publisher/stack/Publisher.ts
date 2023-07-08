import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { SQS } from '../../../Common/SQS/SQS';
import { STACK } from '../../../Common/STACK/STACK';
import { Domain } from '../../Domain/stack/Domain';
import { Lambda } from 'aws-cdk-lib/aws-ses-actions';

export interface PublisherDependencies {
  domain: Domain
}

/** 👉 https://quip.com/sBavA8QtRpXu/-Publisher */
export class Publisher extends STACK {

  public static New(scope: Construct, deps: PublisherDependencies, props?: cdk.StackProps)
  {
    const ret = new Publisher(scope, props);
    ret.addDependency(deps.domain);
    return ret;
  }


  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, Publisher.name, { 
      description: 'Publisher behaviour.',
      ...props
    });

    const subscribers = this.SetUpRegistration();
    const updates = this.SetUpUpdates(subscribers);
    this.SetUpReplays(updates, subscribers);
  }


  private static readonly SUBSCRIBERS = 'Subscribers';
  public static GetSubscribers(stack: STACK): DYNAMO {
    return DYNAMO.Import(stack, Publisher.SUBSCRIBERS);
  }

  private SetUpRegistration(): DYNAMO {

    const subscribers = DYNAMO
      .New(this, 'Subscribers')
      .Export(Publisher.SUBSCRIBERS);

    LAMBDA
      .New(this, 'Unsubscribe')
      .HandlesMessenger('Unsubscribe@Publisher')
      .WritesToDynamoDB(subscribers, 'SUBSCRIBERS');

    LAMBDA
      .New(this, 'Subscribe')
      .HandlesMessenger('Subscribe@Publisher')
      .WritesToDynamoDB(subscribers, 'SUBSCRIBERS');
      
    return subscribers;
  }

  public static GetUpdates(stack: STACK): DYNAMO {
    return DYNAMO.Import(stack, Publisher.UPDATES);
  }

  private static readonly UPDATES = 'Updates';
  private SetUpUpdates(subscribers: DYNAMO): DYNAMO {  
    
    const updates = DYNAMO
      .New(this, Publisher.UPDATES, {
        stream: true,
        dated: true
      });

    LAMBDA
      .New(this, 'Publish')
      .HandlesMessenger('Publish@Publisher')
      .WritesToDynamoDB(updates, 'UPDATES')
      .ReadsFromDynamoDB(subscribers, 'SUBSCRIBERS');

    return updates;
  }


  private static readonly TOKENS = 'Tokens';
  public static GetTokens(stack: STACK): DYNAMO {
    return DYNAMO.Import(stack, Publisher.TOKENS);
  }

  private SetUpReplays(updates: DYNAMO, subscribers: DYNAMO) {

    const tokens = DYNAMO
      .New(this, 'Tokens', { ttl: true })
      .Export(Publisher.TOKENS);

    LAMBDA
      .New(this, 'Replay')
      .ReadsFromDynamoDB(updates, 'UPDATES')
      .WritesToDynamoDB(tokens, 'TOKENS')
      .ReadsFromDynamoDB(subscribers, 'SUBSCRIBERS')
      .HandlesMessenger('Replay@Publisher')
      .PublishesToMessenger();

    LAMBDA
      .New(this, 'Next')
      .HandlesMessenger('Next@Publisher')
      .ReadsFromDynamoDB(updates, 'UPDATES')
      .ReadsFromDynamoDB(subscribers, 'SUBSCRIBERS')
      .WritesToDynamoDB(tokens, 'TOKENS')
      .PublishesToMessenger();

  }


}


