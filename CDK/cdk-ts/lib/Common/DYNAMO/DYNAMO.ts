import * as cdk from 'aws-cdk-lib';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';

//import {AwsCustomResource, AwsCustomResourcePolicy, AwsSdkCall, PhysicalResourceId} from "@aws-cdk/custom-resources";
import {AwsCustomResource, AwsCustomResourcePolicy, AwsSdkCall, PhysicalResourceId} from "aws-cdk-lib/custom-resources";
//import {Effect, PolicyStatement} from "@aws-cdk/aws-iam";
import {Effect, PolicyStatement} from "aws-cdk-lib/aws-iam";
import * as logs from 'aws-cdk-lib/aws-logs';

import { STACK } from '../STACK/STACK';

export interface DYNAMOOptions {
  keyName?: string;
  stream?: boolean;
  ttl?: string;
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
          tableName: `${scope.Name}-${id}`,
          partitionKey: { 
            name: options.keyName ?? 'ID', 
            type: dynamodb.AttributeType.STRING 
          },
          billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
          removalPolicy: cdk.RemovalPolicy.DESTROY,
          stream: options.stream ? 
            dynamodb.StreamViewType.NEW_AND_OLD_IMAGES : undefined,
          timeToLiveAttribute: options.ttl
        });
        
        const ret = new DYNAMO(scope, sup);

        return ret;
    }
    

    public Export(alias: string): DYNAMO {
      new cdk.CfnOutput(this.Super, alias, {
        value: this.Super.tableName,
        exportName: alias,
      });
      new cdk.CfnOutput(this.Super, alias + 'Arn', {
        value: this.Super.tableArn,
        exportName: alias + 'Arn',
      });
      return this;
    }


    public static Import(scope: STACK, alias: string): DYNAMO {
      const name = cdk.Fn.importValue(alias);
      const sup = dynamodb.Table.fromTableName(scope, scope.RandomName('Table'), name);
      const ret = new DYNAMO(scope, sup as cdk.aws_dynamodb.Table);
      return ret;
    }



    // https://github.com/kevinvaningen/cdk-custom-resource-dynamo-insert-example/blob/main/lib/single-insert-custom-resource-construct.ts
    // https://kevin-van-ingen.medium.com/aws-cdk-custom-resources-for-dynamodb-inserts-2d79cb1ae395
    // https://stackoverflow.com/questions/62724486/aws-cdk-dynamodb-initial-data
    // https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.custom_resources.AwsSdkCall.html
    public PutItem(item: any) {
      const table = this.Super;
      const scope = this.Scope;
      const tableName = table.tableName;
      const tableArn = table.tableArn;

      const awsSdkCall: AwsSdkCall = {
        service: 'DynamoDB',
        action: 'putItem',
        physicalResourceId: PhysicalResourceId.of(tableName + '_batch_inserts'),
        parameters: {
          'TableName': tableName,
          'Item': item
        }
      };
      
      new AwsCustomResource(scope, scope.RandomName("Custom"), {
        onCreate: awsSdkCall,
        onUpdate: awsSdkCall,
        logRetention: logs.RetentionDays.ONE_WEEK,
        policy: AwsCustomResourcePolicy.fromStatements([
          new PolicyStatement({
            sid: 'DynamoWriteAccess',
            effect: Effect.ALLOW,
            actions: ['dynamodb:PutItem'],
            resources: [tableArn],
          })
        ]),
        timeout: cdk.Duration.minutes(5)
      });

    }

}

