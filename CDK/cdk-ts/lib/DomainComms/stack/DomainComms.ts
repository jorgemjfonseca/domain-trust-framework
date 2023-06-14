import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { WAF } from '../../Common/Waf/Waf';
import { API } from '../../Common/ApiGW/Api';
import { LAMBDA } from '../../Common/Lambda/Lambda';
import { BUS } from '../../Common/EventBus/EventBus';
import { KEY } from '../../Common/KmsKey/KmsKey';

export class DomainComms extends cdk.Stack {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, DomainComms.name, props);
    
    const waf = WAF.New(this, 'WAFv2');

    API.New(this)
      .AssociateWaf(waf)
      .Export('DomainApi');

    BUS.New(this)
      .Export('DomainBus');

    LAMBDA.New(this, "WrapperFn")
      .Export('DomainWrapperFn');

    const signatureKey = KEY.New(this, 'Key');

    LAMBDA.New(this, "UnwrapperFn")
      .SignsWithKey(signatureKey)
      .Export('DomainUnwrapperFn');

    
  }
}
