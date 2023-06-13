import * as cdk from 'aws-cdk-lib';
import * as sqs from 'aws-cdk-lib/aws-sqs';


export class QUEUE extends sqs.Queue {

    Dlq: sqs.Queue;

    constructor(scope: cdk.Stack , id: string, dlq: sqs.Queue) {

        super(scope, id,{ 
          queueName: scope.stackName+id,
          enforceSSL: true,      
          deadLetterQueue: { 
            maxReceiveCount: 1,
            queue: dlq
          }
        });

        this.Dlq = dlq;
    }
    
}


export class DLQ extends sqs.Queue {
  constructor(scope: cdk.Stack , id: string) {

    super(scope, id,{ 
      queueName: scope.stackName+id
    });

  }
}