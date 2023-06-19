import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { WAF } from '../../../Common/WAF/WAF';
import { API } from '../../../Common/API/API';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { BUS } from '../../../Common/BUS/BUS';
import { KEY } from '../../../Common/KEY/KEY';
import { STACK } from '../../../Common/STACK/STACK';


export class SharedComms extends STACK {

  public static readonly BUS = 'DomainBus';
  public static readonly API = 'DomainApi';
  public static readonly WRAPPER = 'DomainWrapperFn';
  public static readonly UNWRAPPER = 'DomainUnwrapperFn';
  public static readonly KEY_ARN = 'DomainSignatureKey';
  public static readonly KEY_SPEC = 'DomainSignatureKeySpec';

  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, SharedComms.name, props);
    
    const waf = WAF.New(this, 'WAFv2');

    API.New(this)
      .AssociateWaf(waf)
      .Export(SharedComms.API);

    BUS.New(this)
      .Export(SharedComms.BUS);

    LAMBDA.New(this, "WrapperFn")
      .Export(SharedComms.WRAPPER);

    const signatureKey = KEY.NewForDomain(this, 'Key')
      .ExportArn(SharedComms.KEY_ARN)
      .ExportKeySpec(SharedComms.KEY_SPEC);

    LAMBDA.New(this, "UnwrapperFn")
      .SignsWithKey(signatureKey)
      .Export(SharedComms.UNWRAPPER);
    
   

  }
}
