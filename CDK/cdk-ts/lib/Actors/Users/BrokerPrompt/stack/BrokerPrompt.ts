import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../../Common/STACK/STACK';

// https://quip.com/3mKNASbBpnng
export class BrokerPrompt extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, BrokerPrompt.name, props);


  }
}
