import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { S3 } from '../../../Common/S3/S3';
import { STACK } from '../../../Common/STACK/STACK';
import { DomainName } from '../../DomainName/stack/DomainName';
import { APPCONFIG } from '../../../Common/APPCONFIG/APPCONFIG';
import { CUSTOM } from '../../../Common/CUSTOM/CUSTOM';


export interface ManifesterBucketDependencies {
  domainName: DomainName
}

//https://quip.com/BfbEAAFo5aOV/-Manifester
export class ManifesterBucket extends STACK {

  public static readonly VIEWER_FN = 'DomainManifestViewerFn';
  private static readonly CONFIG = 'ManifestConfigOut';

  public static GetViewerFn(scope: STACK) {
    return LAMBDA.Import(scope, this.VIEWER_FN);
  }
  
  public static GetConfigArn(): string {
    return APPCONFIG.ImportArn(ManifesterBucket.CONFIG);
  }

  public static New(scope: Construct, deps: ManifesterBucketDependencies): ManifesterBucket {
    const ret = new ManifesterBucket(scope);
    ret.addDependency(deps.domainName);
    return ret;
  }
 
  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, ManifesterBucket.name, { 
      description: "Create the manifest's config & viewer.",
      ...props
    });
    
    const domainName = DomainName.GetDomainName(this);
    
    // Config
    const appConfig = APPCONFIG
      .NewYaml(this, 'Manifest', `
Identity:
    Domain: ${domainName}
    Name: Random Domain`
      )
      .Export('ManifestConfigOut');

    // VIEWER LAMBDA
    LAMBDA
      .New(this, "ViewerFn")
      .ReadsAppConfig(appConfig)
      .Export(ManifesterBucket.VIEWER_FN);

  }
  
}


//https://quip.com/BfbEAAFo5aOV/-Manifester
/**
 * @deprecated use the AppConfig version instead.
 */
export class ManifesterBucketS3 extends STACK {

  private static readonly BUCKET = 'DomainManifestBucket';
  private static readonly FILE_NAME = 'DomainManifest.yaml';

  public static GetBucket(scope: STACK) {
    return S3.Import(scope, this.BUCKET);
  }

  
  private CreateS3(bucketName: string) {
    const s3 = S3
      .New(this, 'ManifestBucket', { 
        bucketName, 
        versioned: true
      })
      .Export(ManifesterBucketS3.BUCKET);
    return s3;
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, ManifesterBucket.name, { 
      description: "Create the manifest's bucket & viewer.",
      ...props
    });

    const domainName = DomainName.GetDomainName(this);   

    const bucketName = `${'dtfw'}-${domainName}`;
    const s3 = this.CreateS3(bucketName);

    // VIEWER LAMBDA
    LAMBDA
      .New(this, "ViewerFn")
      .ReadsFromS3(s3)
      .AddEnvironment('BUCKET_NAME', bucketName)
      .AddEnvironment('FILE_NAME', ManifesterBucketS3.FILE_NAME)
      .Export(ManifesterBucket.VIEWER_FN);

    // INIT LAMBDA
    const initFn = LAMBDA
      .New(this, 'CfnFn')
      .WritesToS3(s3)
      .AddEnvironment('BUCKET_NAME', bucketName)
      .AddEnvironment('FILE_NAME', ManifesterBucketS3.FILE_NAME)
      .AddEnvironment('DOMAIN_NAME', domainName);
    
    CUSTOM.New('CfnFnCustom', initFn);

  }

  
}
