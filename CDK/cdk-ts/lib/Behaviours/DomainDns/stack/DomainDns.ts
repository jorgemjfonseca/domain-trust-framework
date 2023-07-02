import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { ROUTE53 } from '../../../Common/ROUTE53/ROUTE53';
import { CERTIFICATE } from '../../../Common/CERTIFICATE/CERTIFICATE';
import { STACK } from '../../../Common/STACK/STACK';
import { DomainName } from '../../DomainName/stack/DomainName';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { CUSTOM } from '../../../Common/CUSTOM/CUSTOM';
import { DomainDnsKey } from '../../DomainDnsKey/stack/DomainDnsKey';

export interface DomainDnsDependencies {
  domainName: DomainName
  domainDnsKey: DomainDnsKey
}

export class DomainDns extends STACK {
  
  public static readonly HOSTED_ZONE = 'HostedZone';
  public static readonly CERTIFICATE = 'DomainDnsCertificate';

  public static New(scope: Construct, deps: DomainDnsDependencies): DomainDns {
    const ret = new DomainDns(scope);
    ret.addDependency(deps.domainName);
    ret.addDependency(deps.domainDnsKey);
    return ret;
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, DomainDns.name, {
      description: 'Creates Route53 DnsSec with ACM certificates.',
      ...props
    });

    const domainName = DomainName.GetDomainName(this);
    const dnsSecKey = DomainDnsKey.GetKey(this);
      
    const dns = ROUTE53
      .New(this, 'DNS', domainName)
      .ConfigureDnsSec(dnsSecKey)
      .Export(DomainDns.HOSTED_ZONE);
    
    CERTIFICATE
      .NewByDns(this, "Certificate", dns)
      .Export(this, DomainDns.CERTIFICATE);

    const registererFn = LAMBDA
      .New(this, 'RegistererFn', {
        runtime: LAMBDA.PYTHON_3_10,
        handler: 'index.on_event'
      })
      .GrantRoute53FullAccess()
      .AddEnvironment('domainName', domainName)
      .AddEnvironment('hostedZoneId', dns.Super.hostedZoneId)

    CUSTOM.New('RegistererCfn', registererFn);
    
    this.Export('DomainName', domainName);
    this.Export('HostedZoneId', dns.Super.hostedZoneId)
  }

}
