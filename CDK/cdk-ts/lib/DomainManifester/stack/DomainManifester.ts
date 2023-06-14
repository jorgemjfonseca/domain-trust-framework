import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../Common/Lambda/Lambda';
import { BUS } from '../../Common/EventBus/EventBus';
import { S3 } from '../../Common/S3/S3';

export class DomainManifester extends cdk.Stack {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, DomainManifester.name, props);

    // S3
    const bucket = S3.New(this, "Bucket")
      .CreateCloudFrontDistribution()
      .Export("DomainManifestBucket");
      

    // LAMBDA
    const bus = BUS.Import(this, "DomainBus");
    LAMBDA.New(this, "AlerterFn")
      .TriggeredByS3(bucket)
      .SendsMessagesToBus(bus);

  }
}
