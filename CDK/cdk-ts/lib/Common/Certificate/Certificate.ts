import * as cdk from 'aws-cdk-lib';
import * as acm from 'aws-cdk-lib/aws-certificatemanager';


//https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_certificatemanager-readme.html
export class CERTIFICATE  {

    Super: acm.Certificate;
    
    public static NewByEmail(scope: cdk.Stack, id: string, domainName: string): CERTIFICATE {
        const ret = new CERTIFICATE();

        ret.Super = new acm.Certificate(scope, id, {
          domainName: domainName,
          validation: acm.CertificateValidation.fromEmail(), 
        });
 
        return ret;
    }
    
}