import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { KMS_KEY } from '../../../Common/KEY/KMS_KEY';


// 👉 https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-configuring-dnssec-cmk-requirements.html
export class DomainDnsKey extends STACK {

  private static readonly KEY_ALIAS = 'DnsSecKey';
  private static readonly REGION = 'us-east-1';

  public static GetKey(scope: STACK): KMS_KEY {
    return KMS_KEY.ImportFromRegion(scope, 
      DomainDnsKey.REGION,
      DomainDnsKey.name,
      DomainDnsKey.KEY_ALIAS);
  }
 
  public static New(scope: Construct): DomainDnsKey {
    return new DomainDnsKey(scope);
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, DomainDnsKey.name, {
      ...props,
      description: 'Creates a DnsSec key in Region eu-east-1.',
      env: { region: DomainDnsKey.REGION }
    });

    KMS_KEY
        .NewForDnsSec(this, DomainDnsKey.KEY_ALIAS);

  }
}
