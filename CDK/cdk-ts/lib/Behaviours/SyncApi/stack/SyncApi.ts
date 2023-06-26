import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';


// 👉 https://quip.com/RnO6Ad0BuBSx/-Sync-API
export class SyncApi extends STACK {

  
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, SyncApi.name, props);

  }

}
