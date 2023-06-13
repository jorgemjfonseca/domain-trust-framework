import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { BucketProps } from 'aws-cdk-lib/aws-s3';
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront';
import { S3Origin } from 'aws-cdk-lib/aws-cloudfront-origins';


export class S3 {
 
    Scope: cdk.Stack;
    Super: s3.Bucket;

    public static New(
      scope: cdk.Stack , 
      id: string, 
      props?: BucketProps
    ): S3 {

        const ret = new S3();

        ret.Super = new s3.Bucket(scope, "Bucket", {
          ...props,
          blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
          removalPolicy: cdk.RemovalPolicy.DESTROY
        });

        ret.Scope = scope;

        return ret;
    }


    public CreateCloudFrontDistribution(): S3 {
      
      const originAccessIdentity = new cloudfront
        .OriginAccessIdentity(this.Scope, "Origin", {
          comment: "Only allow CloudFront to access the S3 bucket directly"
        });

      const distribution = new cloudfront.Distribution(this.Scope, "Cloudfront", {
        defaultBehavior: {
          origin: new S3Origin(this.Super, {
            originAccessIdentity
          }),
          allowedMethods: cloudfront.AllowedMethods.ALLOW_ALL,
          cachePolicy: cloudfront.CachePolicy.CACHING_DISABLED
        }
      });

      return this;
    }

}

