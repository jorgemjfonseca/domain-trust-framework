import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { ROUTE53 } from '../../../Common/ROUTE53/ROUTE53';
import { API } from '../../../Common/API/API';
import { CERTIFICATE } from '../../../Common/CERTIFICATE/CERTIFICATE';
import { randomUUID } from 'crypto';
import { SharedComms } from '../../SharedComms/stack/SharedComms';
import { STACK } from '../../../Common/STACK/STACK';

export class SharedDns extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, SharedDns.name, props);
    
    const domainName = randomUUID() + '.dev.dtfw.org';
    const dns = ROUTE53.New(this, 'DNS', domainName);

    const api = API.Import(this, SharedComms.API);
    // Sync Endpoint, https://quip.com/lcSaAX7AiEXL/-Domain#temp:C:RSE573b766d24e74eafbb7015392
    dns.AddTxtRecord('_DTFW.SYNC', '<copy from '+api.Arn+'>');
    // Async Endpoint, https://quip.com/lcSaAX7AiEXL/-Domain#temp:C:RSEb2f72cb4b4054777a7253b335
    dns.AddTxtRecord('_DTFW.ASYNC', '<copy from '+api.Arn+'>');

    dns.AddTxtRecord('_DTFW.SIGN.KEY', '<copy public key from '+cdk.Fn.importValue(SharedComms.KEY_ARN)+'>');
    dns.AddTxtRecord('_DTFW.SIGN.SPEC', '<copy public key from '+cdk.Fn.importValue(SharedComms.KEY_SPEC)+'>');

    CERTIFICATE.NewByEmail(this, "Certificate", domainName);
  }
}
