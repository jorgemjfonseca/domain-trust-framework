import { STACK } from '../STACK/STACK';
import { CONSTRUCT } from '../CONSTRUCT/CONSTRUCT';
import {RemovalPolicy} from "aws-cdk-lib/core";
import {CfnDatabase, CfnTable} from "aws-cdk-lib/aws-timestream";


export interface TIMESTREAMParams {
  /** @default DB */
  databaseName: string;
  /** @default TB */
  tableName: string;
}

// 👉 https://github.com/kevinvaningen/timestream-cdk-example/blob/main/lib/timestream-construct.ts
// 👉 https://kevin-van-ingen.medium.com/aws-timestream-cdk-5e1b7d760828
export class TIMESTREAM extends CONSTRUCT {

  Scope: STACK;
  public readonly Database: CfnDatabase;
  public readonly Table: CfnTable;

  
  public static New(
    scope: STACK, 
    props?: TIMESTREAMParams
  ): TIMESTREAM {

      const ret = new TIMESTREAM(scope, props);

      ret.Scope = scope;

      return ret;
  }
    

  private constructor(scope: STACK, props?: TIMESTREAMParams) {
    super(scope);

    this.Scope = scope;

    this.Database = new CfnDatabase(this, 'Database', {
        databaseName: props?.databaseName ?? 'DB',
    });

    this.Database.applyRemovalPolicy(RemovalPolicy.DESTROY);

    this.Table = new CfnTable(this, 'Table', {
        tableName: props?.tableName ?? 'TB',
        databaseName: props?.databaseName ?? 'DB',
        retentionProperties: {
            memoryStoreRetentionPeriodInHours: (24 * 60).toString(10),
            magneticStoreRetentionPeriodInDays: (365 * 10).toString(10)
        }
    });

    this.Table.node.addDependency(this.Database);
    this.Table.applyRemovalPolicy(RemovalPolicy.DESTROY);
  }


}

