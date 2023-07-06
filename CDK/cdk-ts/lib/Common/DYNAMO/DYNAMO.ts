import * as cdk from 'aws-cdk-lib';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';

//import {AwsCustomResource, AwsCustomResourcePolicy, AwsSdkCall, PhysicalResourceId} from "@aws-cdk/custom-resources";
import {AwsCustomResource, AwsCustomResourcePolicy, AwsSdkCall, PhysicalResourceId} from "aws-cdk-lib/custom-resources";
//import {Effect, PolicyStatement} from "@aws-cdk/aws-iam";
import {Effect, PolicyStatement} from "aws-cdk-lib/aws-iam";
import * as logs from 'aws-cdk-lib/aws-logs';

import { STACK } from '../STACK/STACK';

export interface DYNAMOOptions {
  stream?: boolean;
  ttl?: boolean;
  dated?: boolean,
  filtered?: boolean
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

        const partitionKey = { 
          name: 'ID', 
          type: dynamodb.AttributeType.STRING 
        };

        const stream = options.stream 
          ? dynamodb.StreamViewType.NEW_AND_OLD_IMAGES 
          : undefined;

        const timeToLiveAttribute = options.ttl
          ? 'TTL'
          : undefined;

        const sortKey: cdk.aws_dynamodb.Attribute | undefined = options.dated ? {
            name: 'Timestamp',
            type: dynamodb.AttributeType.STRING 
          }
          : options.filtered ? {
            name: 'Filter',
            type: dynamodb.AttributeType.STRING 
          }
          : undefined;

        const sup = new cdk.aws_dynamodb.Table(scope, `${DYNAMO.name}-${id}`,{ 
          tableName: `${scope.Name}-${id}`,
          partitionKey: partitionKey,
          sortKey: sortKey,
          billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
          removalPolicy: cdk.RemovalPolicy.DESTROY,
          stream: stream,
          timeToLiveAttribute: timeToLiveAttribute
        });
        
        const ret = new DYNAMO(scope, sup);

        return ret;
    }
    

    
    public AddIndex(): DYNAMO {
      // 👉 https://bobbyhadz.com/blog/aws-cdk-add-global-secondary-index-dynamodb
      this.Super.addGlobalSecondaryIndex({
        indexName: 'userIdIndex',
        partitionKey: {name: 'userId', type: dynamodb.AttributeType.STRING},
        sortKey: {name: 'status', type: dynamodb.AttributeType.STRING},
        readCapacity: 1,
        writeCapacity: 1,
        projectionType: dynamodb.ProjectionType.ALL,
      });
      return this;
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
      new cdk.CfnOutput(this.Super, alias + 'Stream', {
        value: this.Super.tableStreamArn + '',
        exportName: alias + 'Stream',
      });
      return this;
    }


    public static Import(scope: STACK, alias: string): DYNAMO {
      const tableName = cdk.Fn.importValue(alias);
     
      /*
      // this doesn't allow to import a table with a Stream.
      // 👉 https://github.com/aws/aws-cdk/issues/7470
      const sup = dynamodb.Table.fromTableName(
        scope, 
        scope.RandomName(alias), 
        tableName);
        */
      
      const tableArn = cdk.Fn.importValue(alias + 'Arn');

      let tableStreamArn: string | undefined
      tableStreamArn = cdk.Fn.importValue(alias + 'Stream');
      if (!tableStreamArn)
        tableStreamArn = undefined  
      
      const sup = dynamodb.Table.fromTableAttributes(
        scope, 
        scope.RandomName(`${DYNAMO.name}-Imported-${alias}`), {
          // tableArn, // only Arn or Name can be provided, not both.
          tableName,
          tableStreamArn
        });

      const ret = new DYNAMO(scope, sup as cdk.aws_dynamodb.Table);
      return ret;
    }



    // 👉 https://github.com/kevinvaningen/cdk-custom-resource-dynamo-insert-example/blob/main/lib/single-insert-custom-resource-construct.ts
    // 👉 https://kevin-van-ingen.medium.com/aws-cdk-custom-resources-for-dynamodb-inserts-2d79cb1ae395
    // 👉 https://stackoverflow.com/questions/62724486/aws-cdk-dynamodb-initial-data
    // 👉 https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.custom_resources.AwsSdkCall.html
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

