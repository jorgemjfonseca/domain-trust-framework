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
    const filter = this.SetUpFilter();
    const updates = this.SetUpUpdates(subscribers, filter);
    this.SetUpReplays(updates, filter);
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


  private static readonly FILTERS = 'Filters';
  private static GetFilterFn(scope: STACK): LAMBDA {
    return LAMBDA.Import(scope, 'FilterFn');
  }
  private SetUpFilter(): SQS {

    const sqs = SQS 
      .New(this, 'FilterSqs');

    const filters = DYNAMO
      .New(this, 'Filters')
      .Export(Publisher.FILTERS);

    LAMBDA
      .New(this, 'Filter')
      .TriggeredBySQS(sqs)
      .ReadsFromDynamoDB(filters, 'FILTERS')
      .PublishesToMessenger()
      .Export('FilterFn');

    // REGISTER EXTENSION
    LAMBDA
      .prototype
      .FiltersPublisher = function() {
        Publisher.FiltersPublisher(this.Scope, this);
        return this;
      };

    return sqs;
  }


  public static FiltersPublisher(
    scope: STACK, 
    fn: LAMBDA) 
  {
    const filters = DYNAMO
      .Import(scope, Publisher.FILTERS);
      
    // Register the function name.
    filters.PutItem({
      'ID': {'S':fn.FunctionName()}
    });

    // Add invoke permission.
    Publisher
      .GetFilterFn(scope)
      .InvokesLambda(fn);
  }


  private static readonly UPDATES = 'Updates';
  private SetUpUpdates(subscribers: DYNAMO, filter: SQS): DYNAMO {  
    
    const updates = DYNAMO
      .New(this, Publisher.UPDATES, {
        stream: true,
        dated: true
      });

    LAMBDA
      .New(this, 'Updated')
      .HandlesMessenger('Updated@Publisher')
      .WritesToDynamoDB(updates, 'UPDATES')
      .ReadsFromDynamoDB(subscribers, 'SUBSCRIBERS')
      .PublishesToQueue(filter, 'FILTER');

    return updates;
  }


  private static readonly TOKENS = 'Tokens';
  public static GetTokens(stack: STACK): DYNAMO {
    return DYNAMO.Import(stack, Publisher.TOKENS);
  }

  private SetUpReplays(updates: DYNAMO, filter: SQS) {

    const tokens = DYNAMO
      .New(this, 'Tokens', { ttl: true })
      .Export(Publisher.TOKENS);

    LAMBDA
      .New(this, 'Replay')
      .ReadsFromDynamoDB(updates, 'UPDATES')
      .WritesToDynamoDB(tokens, 'TOKENS')
      .HandlesMessenger('Replay@Publisher')
      .PublishesToQueue(filter, 'FILTER');

    LAMBDA
      .New(this, 'Next')
      .HandlesMessenger('Next@Publisher')
      .ReadsFromDynamoDB(updates, 'UPDATES')
      .WritesToDynamoDB(tokens, 'TOKENS')
      .PublishesToQueue(filter, 'FILTER');

  }


}



declare module '../../../Common/LAMBDA/LAMBDA' {
  interface LAMBDA {
    FiltersPublisher(): LAMBDA;
  }
}