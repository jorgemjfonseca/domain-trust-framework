import * as cdk from 'aws-cdk-lib';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as targets from 'aws-cdk-lib/aws-events-targets';
import * as events from 'aws-cdk-lib/aws-events';


export class QUEUE {

    Dlq: DLQ;
    Scope: cdk.Stack;
    Super: sqs.Queue;
    

    public static New(
      scope: cdk.Stack , 
      id: string
    ): QUEUE {

        const ret = new QUEUE();

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


    public TriggeredByEventBus(
      eventBus: events.IEventBus,      
      eventPattern: events.EventPattern,     //e.g. { source: ["DTFW"], detailType: ["..."] }
    ): QUEUE 
    {
      const name = this.Super.queueName + eventBus.eventBusName + 'Rule';

      const eventRule = new events.Rule(this.Super, name, {
        ruleName: this.Scope.stackName + name,        
        eventBus: eventBus,
        eventPattern: eventPattern
      });

      eventRule.addTarget(new targets.SqsQueue(this.Super));
    
      return this;
    }
    
}


export class DLQ {

  Super: sqs.Queue;
  Scope: cdk.Stack;

  constructor(scope: cdk.Stack, queue: sqs.Queue) {
    this.Scope = scope;
    this.Super = queue;
  }

  public static New(scope: cdk.Stack, id: string): DLQ {
    
    const sup = new sqs.Queue(scope, id,{ 
      queueName: scope.stackName+id
    });

    const ret = new DLQ(scope, sup);
    return ret;
  }
}