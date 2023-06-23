import * as cdk from 'aws-cdk-lib';
import * as acm from 'aws-cdk-lib/aws-certificatemanager';
import { STACK } from '../STACK/STACK';
import { CONSTRUCT } from '../CONSTRUCT/CONSTRUCT';
import { ROUTE53 } from '../ROUTE53/ROUTE53';


//https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_certificatemanager-readme.html
export class CERTIFICATE extends CONSTRUCT {

    Super: acm.Certificate;
    
    constructor(scope: STACK, sup: acm.Certificate) {
      super(scope);
      this.Super = sup;
    }

    public static NewByEmail(scope: STACK, id: string, domainName: string): CERTIFICATE {
        const sup = new acm.Certificate(scope, id, {
          domainName: domainName,
          validation: acm.CertificateValidation.fromEmail(),
        });
 
        const ret = new CERTIFICATE(scope, sup);
        return ret;
    }

    public static NewByDns(scope: STACK, id: string, zone: ROUTE53): CERTIFICATE {
        const root = new acm.Certificate(scope, scope.RandomName(id), {
          domainName: zone.Super.zoneName,
          validation: acm.CertificateValidation.fromDns(zone.Super), 
        });
        const sup = new acm.Certificate(scope, scope.RandomName(id), {
          domainName: '*.' + zone.Super.zoneName,
          validation: acm.CertificateValidation.fromDns(zone.Super), 
        });
        const ret = new CERTIFICATE(scope, sup);
        return ret;
    }

 
    public Export(scope: STACK, alias: string): CERTIFICATE {
      new cdk.CfnOutput(this.Super, alias, {
        value: this.Super.certificateArn,
        exportName: alias,
      });
      return this;
    }


    public static Import(scope: STACK, alias: string): CERTIFICATE {
      const arn = cdk.Fn.importValue(alias);
      const cert =  acm.Certificate.fromCertificateArn(scope, alias, arn);
      return new CERTIFICATE(scope, cert as acm.Certificate);
    }
    
}