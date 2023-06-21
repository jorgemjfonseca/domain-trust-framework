import * as cdk from 'aws-cdk-lib';
import * as route53 from 'aws-cdk-lib/aws-route53';
import * as targets from 'aws-cdk-lib/aws-route53-targets';
import { CLOUDFRONT } from '../CLOUDFRONT/CLOUDFRONT';
import { KMS_KEY } from '../KEY/KMS_KEY';
import { STACK } from '../STACK/STACK';
import { CONSTRUCT } from '../CONSTRUCT/CONSTRUCT';


//https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_route53-readme.html
export class ROUTE53 extends CONSTRUCT {

    Super: route53.HostedZone;
    
    constructor(scope: STACK) {
      super(scope);
    }

    public static New(scope: STACK, id: string, zoneName: string): ROUTE53 {
        const ret = new ROUTE53(scope);

        ret.Super = new route53.PublicHostedZone(scope, id, {
          zoneName: zoneName,
        });
 
        ret.Scope = scope;

        return ret;
    }

    public AddTxtRecord(name: string, value: string): ROUTE53 {
      new route53.TxtRecord(this.Scope, this.Scope.RandomName('TxtRecord'), {
        zone: this.Super,
        recordName: name, 
        values: [ value ],
        ttl: cdk.Duration.minutes(1),
      });
      return this;
    }

    public AddCNameRecord(name: string, domainName: string) {
      new route53.CnameRecord(this.Scope, name, {
        zone: this.Super,
        recordName: name, 
        domainName: domainName,
        ttl: cdk.Duration.minutes(1),
      });
    }

    public AddCloudFront(name: string, cloudFront: CLOUDFRONT) {
      new route53.AaaaRecord(this.Scope, name, {
        zone: this.Super,
        recordName: name,
        ttl: cdk.Duration.minutes(1),
        target: route53.RecordTarget.fromAlias(
          new targets.CloudFrontTarget(cloudFront.Super)),
      });
    }
    

    public Secure() {
      const dnssecKey = KMS_KEY.NewForDnsSec(this.Scope, "SecureKey");
      dnssecKey.GrantToService('dnssec-route53.amazonaws.com');

      const keySigningKey = new route53.CfnKeySigningKey(this.Scope, 'route-53-key-signing-key', {
        hostedZoneId: this.Super.hostedZoneId,
        keyManagementServiceArn: `arn:aws:kms:us-east-1:${cdk.Aws.ACCOUNT_ID}:alias/${dnssecKey.Alias}`,
        name: 'ExampleComKeySigningKey',
        status: 'ACTIVE',
      });

      const dnssec = new route53.CfnDNSSEC(this.Scope, 'zone-example-com-dnssec', {
        hostedZoneId: this.Super.hostedZoneId
      });
      dnssec.node.addDependency(keySigningKey);

      // continue at https://deepdive.codiply.com/enable-dnssec-signing-in-amazon-route-53-using-aws-cdk
    }

}