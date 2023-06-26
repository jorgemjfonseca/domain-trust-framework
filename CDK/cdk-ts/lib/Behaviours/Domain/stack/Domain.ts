import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';

export class Domain extends STACK {
  

  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, Domain.name, props);
    
  }

}
