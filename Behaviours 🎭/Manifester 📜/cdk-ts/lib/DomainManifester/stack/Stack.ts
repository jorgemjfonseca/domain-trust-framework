import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront';
import { S3Origin } from 'aws-cdk-lib/aws-cloudfront-origins';
import { LAMBDA } from '../../Common/Lambda/Lambda';
import { DLQ } from '../../Common/Queue/Queue';
import * as events from 'aws-cdk-lib/aws-events';

export class DomainManifester extends cdk.Stack {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, DomainManifester.name, props);

    // S3
    const bucket = new s3.Bucket(this, "Bucket", {
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      removalPolicy: cdk.RemovalPolicy.DESTROY
    });

    // CLOUDFRONT
    const originAccessIdentity = new cloudfront.OriginAccessIdentity(this, "Origin", {
      comment: "Only allow CloudFront to access the S3 bucket directly"
    });
    const distribution = new cloudfront.Distribution(this, "Cloudfront", {
      defaultBehavior: {
        origin: new S3Origin(bucket, {
          originAccessIdentity
        }),
        allowedMethods: cloudfront.AllowedMethods.ALLOW_ALL,
        cachePolicy: cloudfront.CachePolicy.CACHING_DISABLED
      }
    });

    // LAMBDA
    const bus = events.EventBus.fromEventBusName(this, 'Bus', 'DomainMessengerBus');
    const alerterDlq = new DLQ(this, "AlerterDlq");
    const alerterLambda = new LAMBDA(this, "Alerter", alerterDlq, {
      runtime: lambda.Runtime.NODEJS_18_X,
      code: lambda.Code.fromAsset('lib/' + DomainManifester.name + '/lambda/alerter'),
      handler: 'exports.handler',
      memorySize: 1024, 
      timeout: cdk.Duration.seconds(30)
    })
    .ConsumeEventsFromS3(bucket)
    .SendMessagesToBus(bus);

  }
}
