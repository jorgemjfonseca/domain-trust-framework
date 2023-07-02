import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { STACK } from '../../../Common/STACK/STACK';
import { DomainName } from '../../DomainName/stack/DomainName';
import { APPCONFIG } from '../../../Common/APPCONFIG/APPCONFIG';


export interface ManifesterBucketDependencies {
  domainName: DomainName
}

//https://quip.com/BfbEAAFo5aOV/-Manifester
export class ManifesterBucket extends STACK {

  private static readonly JSON_VIEWER = 'DomainManifestJsonViewer';
  private static readonly YAML_VIEWER = 'DomainManifestYamlViewer';
  private static readonly VIEWER_FN = 'DomainManifestViewerFn';
  private static readonly CONFIG = 'ManifestConfigOut';

  public static GetViewerFn(scope: STACK) {
    return LAMBDA.Import(scope, this.VIEWER_FN);
  }

  public static GetYamlViewer(scope: STACK) {
    return LAMBDA.Import(scope, this.YAML_VIEWER);
  }

  public static GetJsonViewer(scope: STACK) {
    return LAMBDA.Import(scope, this.JSON_VIEWER);
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
      .New(this, "DefaultViewer")
      .ReadsAppConfig(appConfig)
      .Export(ManifesterBucket.VIEWER_FN);

    LAMBDA
      .New(this, "JsonViewer")
      .ReadsAppConfig(appConfig)
      .Export(ManifesterBucket.JSON_VIEWER);

    LAMBDA
      .New(this, "YamlViewer")
      .ReadsAppConfig(appConfig)
      .Export(ManifesterBucket.YAML_VIEWER);

  }
  
}
