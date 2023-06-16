import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { ROUTE53 } from '../../../Common/Route53/Route53';
import { API } from '../../../Common/ApiGW/Api';
import { KEY } from '../../../Common/KmsKey/KmsKey';
import { CERTIFICATE } from '../../../Common/Certificate/Certificate';
import { randomUUID } from 'crypto';

export class DomainDNS extends cdk.Stack {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, DomainDNS.name, props);
    
    const domainName = randomUUID() + '.dev.dtfw.org';
    const dns = ROUTE53.New(this, 'DNS', domainName);

    const api = API.Import(this, 'DomainApi');
    // Sync Endpoint, https://quip.com/lcSaAX7AiEXL/-Domain#temp:C:RSE573b766d24e74eafbb7015392
    dns.AddTxtRecord('_DTFW.SYNC', '<copy from '+api.Arn+'>');
    // Async Endpoint, https://quip.com/lcSaAX7AiEXL/-Domain#temp:C:RSEb2f72cb4b4054777a7253b335
    dns.AddTxtRecord('_DTFW.ASYNC', '<copy from '+api.Arn+'>');

    dns.AddTxtRecord('_DTFW.SIGN.KEY', '<copy public key from '+cdk.Fn.importValue('DomainSignatureKey')+'>');
    dns.AddTxtRecord('_DTFW.SIGN.SPEC', '<copy public key from '+cdk.Fn.importValue('DomainSignatureKeySpec')+'>');

    CERTIFICATE.NewByEmail(this, "Certificate", domainName);
  }
}
