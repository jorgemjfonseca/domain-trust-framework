import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { S3 } from '../../../Common/S3/S3';
import { STACK } from '../../../Common/STACK/STACK';

//https://quip.com/BfbEAAFo5aOV/-Manifester
export class Manifester extends STACK {

  public static readonly BUCKET = 'DomainManifestBucket';

  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, Manifester.name, props);

    // S3
    const s3 = S3.New(this, "ManifestBucket")
      .CreateCloudFrontDistribution()
      .Export(Manifester.BUCKET);      

    // INIT LAMBDA
    LAMBDA.New(this, "InitFn")
      .WritesToS3(s3)
      .Export("ManifesterInitFn")

    // ALERT LAMBDA
    LAMBDA.New(this, "AlerterFn")
      .TriggeredByS3(s3)
      .PublishesToMessenger();

  }
}
