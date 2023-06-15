import * as cdk from 'aws-cdk-lib';
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront';
import { S3Origin } from 'aws-cdk-lib/aws-cloudfront-origins';
import { S3 } from '../S3/S3';

export class CLOUDFRONT {

    Super: cloudfront.Distribution;
    Scope: cdk.Stack;

    constructor(scope: cdk.Stack, sup: cloudfront.Distribution)
    {
      this.Scope = scope;
      this.Super = sup;
    }

    public static NewForS3(scope: cdk.Stack, s3: S3) {

      const originAccessIdentity = new cloudfront
        .OriginAccessIdentity(scope, "Origin", {
          comment: "Only allow CloudFront to access the S3 bucket directly"
        });

      const distribution = new cloudfront.Distribution(scope, "Cloudfront", {
        defaultBehavior: {
          origin: new S3Origin(s3.Super, {
            originAccessIdentity
          }),
          allowedMethods: cloudfront.AllowedMethods.ALLOW_ALL,
          cachePolicy: cloudfront.CachePolicy.CACHING_DISABLED
        }
      });

      const ret = new CLOUDFRONT(scope, distribution);
      return ret;
    }

    public Export(alias: string): CLOUDFRONT {
      
      new cdk.CfnOutput(this.Super, alias, {
        value: this.Super.distributionDomainName,
        exportName: alias,
      });

      return this;
    }
    
}