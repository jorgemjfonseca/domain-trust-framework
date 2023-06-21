import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { WAF } from '../../../Common/WAF/WAF';
import { API } from '../../../Common/API/API';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { BUS } from '../../../Common/BUS/BUS';
import { KMS_KEY } from '../../../Common/KEY/KMS_KEY';
import { STACK } from '../../../Common/STACK/STACK';
import { randomUUID } from 'crypto';
import { EC2_KEY } from '../../../Common/KEY/EC2_KEY';

export class SharedComms extends STACK {


  public static readonly BUS = 'DomainBus';
  public static readonly API = 'DomainApi';
  public static readonly WRAPPER = 'DomainWrapperFn';
  public static readonly UNWRAPPER = 'DomainUnwrapperFn';
  public static readonly SIGNATURE_KEY = 'DomainSignatureKey';
  public static readonly DOMAIN_NAME = 'DomainName';

  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, SharedComms.name, props);
    
    this.Export(
      SharedComms.DOMAIN_NAME, 
      randomUUID() + '.dev.dtfw.org');

    const waf = WAF
      .New(this, 'WAFv2');

    API.New(this)
      .AssociateWaf(waf)
      .Export(SharedComms.API);

    BUS.New(this)
      .Export(SharedComms.BUS);

    LAMBDA.New(this, "WrapperFn")
      .Export(SharedComms.WRAPPER);

    const signatureKey = KMS_KEY.NewForDomain(this, 'Key')
      .Export(SharedComms.SIGNATURE_KEY);

    LAMBDA.New(this, "UnwrapperFn")
      .SignsWithKmsKey(signatureKey)
      .Export(SharedComms.UNWRAPPER);
    

  }
}
