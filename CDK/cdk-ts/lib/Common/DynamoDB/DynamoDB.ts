import * as cdk from 'aws-cdk-lib';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';

export interface DYNAMOOptions {
  keyName?: string;
  stream?: boolean;
}

export class DYNAMO {

    Scope: cdk.Stack;
    Super: cdk.aws_dynamodb.Table;
    
    

    public static New(
      scope: cdk.Stack, 
      id: string,
      options: DYNAMOOptions = {}
    ): DYNAMO {

        const ret = new DYNAMO();

        ret.Super = new cdk.aws_dynamodb.Table(scope, id,{ 
          tableName: scope.stackName+id,
          partitionKey: { 
            name: options.keyName ?? 'ID', 
            type: dynamodb.AttributeType.STRING 
          },
          billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
          removalPolicy: cdk.RemovalPolicy.DESTROY,
          stream: options.stream ? 
            dynamodb.StreamViewType.NEW_AND_OLD_IMAGES : undefined
        });

        return ret;
    }
    
}

