import * as cdk from 'aws-cdk-lib';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as targets from 'aws-cdk-lib/aws-events-targets';
import * as events from 'aws-cdk-lib/aws-events';
import { STACK } from '../STACK/STACK';


export class SQS {

    Dlq: DLQ;
    Scope: STACK;
    Super: sqs.Queue;
    

    public static New(
      scope: STACK , 
      id: string
    ): SQS {

        const ret = new SQS();

        const dlq = DLQ.New(scope, id + "DLQ");

        ret.Super = new sqs.Queue(scope, id,{ 
          queueName: scope.stackName+id,
          enforceSSL: true,      
          deadLetterQueue: { 
            maxReceiveCount: 1,
            queue: dlq.Super
          }
        });

        ret.Scope = scope;
        ret.Dlq = dlq;

        return ret;
    }


    public TriggeredByBus(
      eventBus: events.IEventBus,     
      // e.g. { source: ["CustomEvent"], detailType: ["CREATE", "UPDATE", "DELETE"] } 
      // eventPattern: events.EventPattern,     
      detailType: string
    ): SQS 
    {
      const name = this.Super.queueName + eventBus.eventBusName + 'Rule';

      const eventRule = new events.Rule(this.Super, name, {
        ruleName: this.Scope.stackName + name,        
        eventBus: eventBus,
        eventPattern: { 
          //source: ["CustomEvent"], 
          detailType: [ detailType ]
        } 
      });

      eventRule.addTarget(new targets.SqsQueue(this.Super));
    
      return this;
    }
    
}


export class DLQ {

  Super: sqs.Queue;
  Scope: STACK;

  constructor(scope: STACK, queue: sqs.Queue) {
    this.Scope = scope;
    this.Super = queue;
  }

  public static New(scope: STACK, id: string): DLQ {
    
    const sup = new sqs.Queue(scope, id,{ 
      queueName: scope.stackName+id
    });

    const ret = new DLQ(scope, sup);
    return ret;
  }
}