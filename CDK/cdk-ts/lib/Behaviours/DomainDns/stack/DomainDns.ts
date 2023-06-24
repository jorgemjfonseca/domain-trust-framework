import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { ROUTE53 } from '../../../Common/ROUTE53/ROUTE53';
import { CERTIFICATE } from '../../../Common/CERTIFICATE/CERTIFICATE';
import { STACK } from '../../../Common/STACK/STACK';
import { KMS_KEY } from '../../../Common/KEY/KMS_KEY';
import { CUSTOM } from '../../../Common/CUSTOM/CUSTOM';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { randomUUID } from 'crypto';


export class DomainDns extends STACK {
  
  public static readonly HOSTED_ZONE = 'HostedZone';
  public static readonly DOMAIN_NAME = 'DomainName';
  public static readonly KEY = 'DomainDnsKey';
  public static readonly CERTIFICATE = 'DomainDnsCertificate';

  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, DomainDns.name, props);

    const domainName = randomUUID() + '.dev.dtfw.org';

    this.Export(
      DomainDns.DOMAIN_NAME, 
      domainName);
    
    const dkimRecordName = `dtfw._domainkey.${domainName}`
    const dns = ROUTE53
      .New(this, 'DNS', domainName)
      .AddTxtRecord(dkimRecordName, `k=rsa;p=?;`)
      .Export(DomainDns.HOSTED_ZONE);

    const setDkim = LAMBDA
      .New(this, 'SetDkim', {
        runtime: LAMBDA.PYTHON_3_10,
        handler: 'index.on_event'
      })
      .GrantRoute53FullAccess()
      .GrantCloudFormationReadOnlyAccess()
      .GrantKeyManagementServicePowerUser();

    const key = KMS_KEY
      .NewForDomain(this, 'Key')
      .Export(DomainDns.KEY);
    
    CUSTOM
      .New('Custom', setDkim, {
        domainName: domainName,
        hostedZoneId: dns.Super.hostedZoneId,
        hostedZoneNameServers: dns.Super.hostedZoneNameServers,
        signatureKeyArn: key.Super.keyArn,
        dkimRecordName: dkimRecordName
      });

    CERTIFICATE
      .NewByDns(this, "Certificate", dns)
      .Export(this, DomainDns.CERTIFICATE);
    
  }
}
