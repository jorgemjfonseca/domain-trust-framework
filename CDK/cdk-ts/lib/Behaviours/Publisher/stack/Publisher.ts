import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { STACK } from '../../../Common/STACK/STACK';
import { Domain } from '../../Domain/stack/Domain';

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


  private Subscribers: DYNAMO;
  private Updates: DYNAMO;
  private Domains: DYNAMO;
  private Correlations: DYNAMO;
  private Tokens: DYNAMO;

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, Publisher.name, { 
      description: 'Publisher behaviour.',
      ...props
    });

    this.SetUpRegistration();
    this.SetUpUpdates();
    this.SetUpReplays();
  }


  // =================================================
  // REGISTRATION
  // =================================================

  private static readonly SUBSCRIBERS = 'Subscribers';
  public static GetSubscribers(stack: STACK): DYNAMO {
    return DYNAMO.Import(stack, Publisher.SUBSCRIBERS);
  }

  private SetUpRegistration() {

    this.Subscribers = DYNAMO
      .New(this, 'Subscribers')
      .Export(Publisher.SUBSCRIBERS);

    LAMBDA
      .New(this, 'Unsubscribe')
      .HandlesMessenger('Unsubscribe@Publisher')
      .WritesToDynamoDB(this.Subscribers, 'SUBSCRIBERS');

    LAMBDA
      .New(this, 'Subscribe')
      .HandlesMessenger('Subscribe@Publisher')
      .WritesToDynamoDB(this.Subscribers, 'SUBSCRIBERS');
  }


  // =================================================
  // UPDATES
  // =================================================

  public static GetPublisher(stack: STACK): LAMBDA {
    return LAMBDA.Import(stack, 'Publisher');
  }

  private static readonly UPDATES = 'Updates';
  private SetUpUpdates() {  
    
    this.Updates = DYNAMO
      .New(this, Publisher.UPDATES, {
        stream: true,
        dated: true
      });

    this.Domains = DYNAMO
      .New(this, 'Domains', {
        dated: true
      });

    this.Correlations = DYNAMO
      .New(this, 'Correlations', {
        ttl: true
      });

    LAMBDA
      .New(this, 'Publish')
      .HandlesMessenger('Publish@Publisher')
      .ReadsFromDynamoDB(this.Subscribers, 'SUBSCRIBERS')
      .WritesToDynamoDB(this.Updates, 'UPDATES')
      .WritesToDynamoDB(this.Domains, 'DOMAINS')
      .WritesToDynamoDB(this.Correlations, 'CORRRELATIONS')
      .PublishesToMessenger()
      .Export('Publisher');
  }


  // =================================================
  // REPLAYS
  // =================================================

  private static readonly TOKENS = 'Tokens';
  public static GetTokens(stack: STACK): DYNAMO {
    return DYNAMO.Import(stack, Publisher.TOKENS);
  }

  private SetUpReplays() {

    this.Tokens = DYNAMO
      .New(this, 'Tokens', { ttl: true })
      .Export(Publisher.TOKENS);

    LAMBDA
      .New(this, 'Replay')
      .ReadsFromDynamoDB(this.Updates, 'UPDATES')
      .ReadsFromDynamoDB(this.Domains, 'DOMAINS')
      .WritesToDynamoDB(this.Tokens, 'TOKENS')
      .ReadsFromDynamoDB(this.Subscribers, 'SUBSCRIBERS')
      .HandlesMessenger('Replay@Publisher')
      .PublishesToMessenger();

    LAMBDA
      .New(this, 'Next')
      .HandlesMessenger('Next@Publisher')
      .ReadsFromDynamoDB(this.Updates, 'UPDATES')
      .ReadsFromDynamoDB(this.Domains, 'DOMAINS')
      .ReadsFromDynamoDB(this.Subscribers, 'SUBSCRIBERS')
      .WritesToDynamoDB(this.Tokens, 'TOKENS')
      .PublishesToMessenger();

  }


}


