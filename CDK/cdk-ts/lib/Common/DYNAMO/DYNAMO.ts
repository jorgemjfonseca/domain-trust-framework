import * as cdk from 'aws-cdk-lib';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import { STACK } from '../STACK/STACK';

export interface DYNAMOOptions {
  keyName?: string;
  stream?: boolean;
}

export class DYNAMO {

    Scope: STACK;
    Super: cdk.aws_dynamodb.Table;
    
    
    constructor(scope: STACK, sup: cdk.aws_dynamodb.Table) {
      this.Scope = scope;
      this.Super = sup;
    }


    public static New(
      scope: STACK, 
      id: string,
      options: DYNAMOOptions = {}
    ): DYNAMO {

        const sup = new cdk.aws_dynamodb.Table(scope, id,{ 
          tableName: scope.stackName + id,
          partitionKey: { 
            name: options.keyName ?? 'ID', 
            type: dynamodb.AttributeType.STRING 
          },
          billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
          removalPolicy: cdk.RemovalPolicy.DESTROY,
          stream: options.stream ? 
            dynamodb.StreamViewType.NEW_AND_OLD_IMAGES : undefined
        });

        const ret = new DYNAMO(scope, sup);

        return ret;
    }
    

    public Export(alias: string): DYNAMO {
      new cdk.CfnOutput(this.Super, alias, {
        value: this.Super.tableName,
        exportName: alias,
      });
      return this;
    }


    public static Import(scope: STACK, alias: string): DYNAMO {
      const name = cdk.Fn.importValue(alias);
      const sup = dynamodb.Table.fromTableName(scope, alias, name);
      const ret = new DYNAMO(scope, sup as cdk.aws_dynamodb.Table);
      return ret;
    }

}

