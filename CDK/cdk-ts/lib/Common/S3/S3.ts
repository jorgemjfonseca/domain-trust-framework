import * as cdk from 'aws-cdk-lib';
import * as path from 'path';
import * as s3 from 'aws-cdk-lib/aws-s3';
import s3deploy = require('aws-cdk-lib/aws-s3-deployment');
import { BucketProps } from 'aws-cdk-lib/aws-s3';
import { CLOUDFRONT } from '../CLOUDFRONT/CLOUDFRONT';
import { STACK } from '../STACK/STACK';

export class S3 {
 
    Scope: STACK;
    Super: s3.Bucket;
    Distribution?: CLOUDFRONT;

    private constructor(scope: STACK, sup: s3.Bucket) {
      this.Scope = scope;
      this.Super = sup;
    }

    public static New(
      scope: STACK , 
      id: string, 
      props?: BucketProps
    ): S3 {

        const sup = new s3.Bucket(scope, `${scope.Name}-${id}`, {
          blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
          removalPolicy: cdk.RemovalPolicy.DESTROY,
          autoDeleteObjects: true,
          ...props,
        });

        const ret = new S3(scope, sup);
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


    public static Import(stack: STACK, alias: string): S3 {
      const name = cdk.Fn.importValue(alias);
      const buc = s3.Bucket.fromBucketName(stack, alias, name) as s3.Bucket;
      const ret = new S3(stack, buc);
      return ret;
    }

    public AddFiles() : S3 {
      const folder = path.join(S3.CallerDirname(), '../s3');
      new s3deploy.BucketDeployment(this.Scope, 'DeployFiles', {
        sources: [s3deploy.Source.asset(folder)], 
        // 'folder' contains your empty files at the right locations
        destinationBucket: this.Super,
      });
      return this;
    }

    public static CallerDirname({ depth = 1 } = {}): string {
      if (typeof depth !== 'number' || depth < 1 || Math.floor(depth) !== depth)
        throw new Error('Depth must be a positive integer.');
    
      /* Start borrowed/modified code */
      // https://github.com/sindresorhus/callsites/blob/master/index.js
      const _ = Error.prepareStackTrace;
      Error.prepareStackTrace = (_, stack) => stack;
      const stack = new Error().stack!.slice(1);
      Error.prepareStackTrace = _;
    
      // https://github.com/sindresorhus/caller-callsite/blob/master/index.js
      const caller = (stack as any)
        .find((c: NodeJS.CallSite) => 
          //c.getTypeName() !== null &&
          path.dirname(c.getFileName()+'').includes('stack'));
      /* End borrowed/modified code */
    
      return path.dirname(caller.getFileName());
    }

}

