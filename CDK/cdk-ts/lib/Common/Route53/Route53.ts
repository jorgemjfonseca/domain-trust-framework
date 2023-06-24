import * as cdk from 'aws-cdk-lib';
import * as route53 from 'aws-cdk-lib/aws-route53';
import * as targets from 'aws-cdk-lib/aws-route53-targets';
import { CLOUDFRONT } from '../CLOUDFRONT/CLOUDFRONT';
import { KMS_KEY } from '../KEY/KMS_KEY';
import { STACK } from '../STACK/STACK';
import { CONSTRUCT } from '../CONSTRUCT/CONSTRUCT';
import { API } from '../API/API';


// 👉 https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_route53-readme.html
export class ROUTE53 extends CONSTRUCT {

    Super: route53.HostedZone;
    
    constructor(scope: STACK, sup: route53.HostedZone) {
      super(scope);
      this.Super = sup;
    }

    public static New(scope: STACK, id: string, zoneName: string): ROUTE53 {
        const sup = new route53.PublicHostedZone(scope, id, {
          zoneName: zoneName,
        });
 
        const ret = new ROUTE53(scope, sup);
        return ret;
    }

    // Exports to a parameter.
    public Export(alias: string): ROUTE53 {
      new cdk.CfnOutput(this.Super, this.Scope.RandomName('HostedZoneID'), {
        value: this.Super.hostedZoneId,
        exportName: alias+'ID',
      });
      new cdk.CfnOutput(this.Super, this.Scope.RandomName('HostedZoneName'), {
        value: this.Super.hostedZoneId,
        exportName: alias+'Name',
      });
      return this;
    }


    /**
     * @deprecated Throws 'Cannot determine scope for context provider hosted-zone'. Use ImportFromDomainName() instead.
     */
    public static ImportFromAlias(scope: STACK, alias: string): ROUTE53 {
      const hostedZoneId = cdk.Fn.importValue(alias+'ID');
      const hostedZoneName = cdk.Fn.importValue(alias+'Name');
      
      //const sup = ROUTE53.FromLookup(scope, hostedZoneName);
      const sup = ROUTE53
        .FromHostedZoneAttributes(scope, hostedZoneId, hostedZoneName);

      return new ROUTE53(scope, sup);
    }


    /**
     * @deprecated 
     *  Throws 'Cannot determine scope for context provider hosted-zone'. 
     *  Use FromHostedZoneAttributes() instead.
     */
    public static ImportFromDomainName(scope: STACK, hostedZoneName: string): ROUTE53 {
      const sup = ROUTE53.FromLookup(scope, hostedZoneName);
      return new ROUTE53(scope, sup);
    }

    
    /**
     * @deprecated 
     *  This doesnt support API Gateway Custom Domains, use FromLookup() instead
     */
    private static FromHostedZoneAttributes(
      scope: STACK, 
      hostedZoneId: string,
      hostedZoneName: string
    ): route53.HostedZone {
      return route53.HostedZone
        .fromHostedZoneAttributes(scope, hostedZoneName, {
          hostedZoneId: hostedZoneId,
          zoneName: hostedZoneName
        }) as route53.HostedZone;
    }
    

    /**
     * @deprecated 
     *  Throws 'Cannot determine scope for context provider hosted-zone' 
     *  when the hosted zone name comes from a parameter.
     *  In that case, use FromHostedZoneAttributes() instead.
     *  Problem details at https://github.com/aws/aws-cdk/issues/6289#issuecomment-587361047
     *  Source code at https://github.com/aws/aws-cdk/blob/4e72d1e9f00ff464c9e645fe55f9178e30ad44df/packages/%40aws-cdk/aws-route53/lib/hosted-zone.ts#L122-L125
     */
    private static FromLookup(
      scope: STACK, 
      hostedZoneName: string
    ): route53.HostedZone {
      // This requires Stack.Prop.Env to be defined.
      return route53.HostedZone.fromLookup(scope, 'Zone', {
        domainName: hostedZoneName,
        privateZone: false,
      }) as route53.HostedZone;
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
      new route53.CnameRecord(this.Scope, this.Scope.RandomName('CNAME'), {
        zone: this.Super,
        recordName: name, 
        domainName: domainName,
        ttl: cdk.Duration.minutes(1),
      });
    }

    public AddCloudFront(name: string, cloudFront: CLOUDFRONT) {
      new route53.AaaaRecord(this.Scope, this.Scope.RandomName('CLOUDFRONT'), {
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

      // continue at 👉 https://deepdive.codiply.com/enable-dnssec-signing-in-amazon-route-53-using-aws-cdk
    }


    public BindApiGateway(api:API, domainName: string) {
      throw Error('Not implemented');
    }

}