import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { Manifester } from '../../Manifester/stack/Manifester';
import { Messenger } from '../../Messenger/stack/Messenger';
import { SyncApi } from '../../SyncApi/stack/SyncApi';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { DynamoAttributeValue } from 'aws-cdk-lib/aws-stepfunctions-tasks';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';

export interface DomainDependencies {
  manifester: Manifester,
  syncApi: SyncApi,
  messenger: Messenger
};

/** 👉 https://quip.com/lcSaAX7AiEXL/-Domain */
export class Domain extends STACK {


  private static readonly HANDLERS = 'Handlers';
  
  public static New(scope: Construct, deps: DomainDependencies): Domain {
    const ret = new Domain(scope);
    ret.addDependency(deps.manifester);
    ret.addDependency(deps.syncApi);
    ret.addDependency(deps.messenger);
    return ret;
  }


  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, Domain.name, { 
      description: 'Full independent domain.',
      ...props
    });
    
    DYNAMO
      .New(this, Domain.HANDLERS)
      .Export(Domain.HANDLERS);

    LAMBDA.prototype.InvokesHandler = 
      function(event: string) {
        Domain.RaisesEvent(this, event);
        return this;
      };

  }


  /** Registers an event to be handled by HANDLER.Trigger */
  public static RaisesEvent(
    fn: LAMBDA, 
    event: string)
  {
    const handlers = DYNAMO
      .Import(fn.Scope, Domain.HANDLERS);
      
    handlers.PutItem({
      'ID': DynamoAttributeValue.fromString(event),
      'Lambdas':  DynamoAttributeValue.fromList([])
    });

    fn.ReadsFromDynamoDB(handlers, 'HANDLERS');
    fn.InvokesLambdas();
  }

}


declare module '../../../Common/LAMBDA/LAMBDA' {
  interface LAMBDA {

    /** 👉 Registers an event to be handled in python by HANDLER.Trigger() */
    InvokesHandler(event: string): LAMBDA;

  }
}