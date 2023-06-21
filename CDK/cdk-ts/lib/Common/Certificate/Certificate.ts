import * as acm from 'aws-cdk-lib/aws-certificatemanager';
import { STACK } from '../STACK/STACK';
import { CONSTRUCT } from '../CONSTRUCT/CONSTRUCT';
import * as route53 from 'aws-cdk-lib/aws-route53';
import { ROUTE53 } from '../ROUTE53/ROUTE53';


//https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_certificatemanager-readme.html
export class CERTIFICATE extends CONSTRUCT {

    Super: acm.Certificate;
    
    constructor(scope: STACK) {
      super(scope);
    }

    public static NewByEmail(scope: STACK, id: string, domainName: string): CERTIFICATE {
        const ret = new CERTIFICATE(scope);

        ret.Super = new acm.Certificate(ret, id, {
          domainName: domainName,
          validation: acm.CertificateValidation.fromEmail(),
        });
 
        return ret;
    }

    public static NewByDns(scope: STACK, id: string, zone: ROUTE53): CERTIFICATE {
        const ret = new CERTIFICATE(scope);

        ret.Super = new acm.Certificate(scope, id, {
          domainName: zone.Super.zoneName,
          validation: acm.CertificateValidation.fromDns(zone.Super), 
        });

        return ret;
  }
    
}