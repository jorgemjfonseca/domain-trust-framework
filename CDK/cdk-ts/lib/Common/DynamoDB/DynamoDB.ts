import * as cdk from 'aws-cdk-lib';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';


export class DYNAMO {

    Scope: cdk.Stack;
    Super: cdk.aws_dynamodb.Table;
    
    public static New(
      scope: cdk.Stack, 
      id: string,
      keyName: string = 'ID'
    ): DYNAMO {

        const ret = new DYNAMO();

        ret.Super = new cdk.aws_dynamodb.Table(scope, id,{ 
          tableName: scope.stackName+id,
          partitionKey: { name: keyName, type: dynamodb.AttributeType.STRING },
          billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
          removalPolicy: cdk.RemovalPolicy.DESTROY
        });

        return ret;
    }
    
}

