import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { ROUTE53 } from '../../../Common/ROUTE53/ROUTE53';
import { CERTIFICATE } from '../../../Common/CERTIFICATE/CERTIFICATE';
import { STACK } from '../../../Common/STACK/STACK';
import { DomainName } from '../../DomainName/stack/DomainName';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { CUSTOM } from '../../../Common/CUSTOM/CUSTOM';

export class DomainDns extends STACK {
  
  public static readonly HOSTED_ZONE = 'HostedZone';
  public static readonly CERTIFICATE = 'DomainDnsCertificate';

  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, DomainDns.name, {
      description: 'Creates Route52, activates ACM certificates.',
      ...props
    });

    const domainName = DomainName.GetDomainName(this);
      
    const dns = ROUTE53
      .New(this, 'DNS', domainName)
      .Export(DomainDns.HOSTED_ZONE);
    
    CERTIFICATE
      .NewByDns(this, "Certificate", dns)
      .Export(this, DomainDns.CERTIFICATE);

    const registererFn = LAMBDA
      .New(this, 'RegistererFn', {
        runtime: LAMBDA.PYTHON_3_10,
        handler: 'index.on_event'
      })
      .GrantRoute53FullAccess();

    CUSTOM
      .New('Custom', registererFn, {
        domainName: domainName,
        hostedZoneId: dns.Super.hostedZoneId,
        hostedZoneNameServers: dns.Super.hostedZoneNameServers
      });
    
  }

}
