import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { BucketProps } from 'aws-cdk-lib/aws-s3';
import { CLOUDFRONT } from '../CLOUDFRONT/CLOUDFRONT';
import { STACK } from '../STACK/STACK';

export class S3 {
 
    Scope: STACK;
    Super: s3.Bucket;
    Distribution: CLOUDFRONT;

    public static New(
      scope: STACK , 
      id: string, 
      props?: BucketProps
    ): S3 {

        const ret = new S3();
        
        ret.Super = new s3.Bucket(scope, `${scope.Name}-${id}`, {
          ...props,
          blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
          removalPolicy: cdk.RemovalPolicy.DESTROY,
          autoDeleteObjects: true
        });

        ret.Scope = scope;

        return ret;
    }


    public CreateCloudFrontDistribution(): S3 {
      this.Distribution = CLOUDFRONT.NewForS3(this.Scope, this);
      return this;
    }


    public Export(alias: string): S3 {
      
      new cdk.CfnOutput(this.Super, alias, {
        value: this.Super.bucketName,
        exportName: alias,
      });

      this.Distribution?.Export(alias + 'Distribution')
      
      return this;
    }

}

