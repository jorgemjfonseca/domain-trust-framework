import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as events from 'aws-cdk-lib/aws-events';
import * as targets from 'aws-cdk-lib/aws-events-targets';
import { WAF, WebACLAssociation } from '../../Common/Waf/Waf';
import * as kms from 'aws-cdk-lib/aws-kms';
import { API } from '../../Common/ApiGW/Api';
import { DLQ, QUEUE } from '../../Common/Queue/Queue';
import { LAMBDA } from '../../Common/Lambda/Lambda';

export class DomainSyncAPI extends cdk.Stack {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, DomainSyncAPI.name, props);

    
   
  }
}
