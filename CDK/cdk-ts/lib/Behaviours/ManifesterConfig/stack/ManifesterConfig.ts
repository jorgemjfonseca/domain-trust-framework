import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { STACK } from '../../../Common/STACK/STACK';
import { DomainName } from '../../DomainName/stack/DomainName';
import { APPCONFIG } from '../../../Common/APPCONFIG/APPCONFIG';


export interface ManifesterConfigDependencies {
  domainName: DomainName
}

//https://quip.com/BfbEAAFo5aOV/-Manifester
export class ManifesterConfig extends STACK {

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
    return APPCONFIG.ImportArn(ManifesterConfig.CONFIG);
  }

  public static New(scope: Construct, deps: ManifesterConfigDependencies): ManifesterConfig {
    const ret = new ManifesterConfig(scope);
    ret.addDependency(deps.domainName);
    return ret;
  }
 
  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, ManifesterConfig.name, { 
      description: "Create the manifest's config & viewer.",
      ...props
    });
    
    const domainName = DomainName.GetDomainName(this);
    
    // Config
    const appConfig = APPCONFIG
      .NewYaml(this, 'Manifest', `
Identity:
    Domain: ${domainName}
    Name: Random Domain
    SmallIcon: 'https://picsum.photos/20/20'
    BigIcon: 'https://picsum.photos/100/100'
    Translations: 
      - Language: en-us
        Translation: Random Domain
      - Language: pt-br
        Translation: Domínio Aleatório`)
      .Export('ManifestConfigOut');

    // VIEWER LAMBDA
    LAMBDA
      .New(this, "DefaultViewer")
      .ReadsAppConfig(appConfig)
      .Export(ManifesterConfig.VIEWER_FN);

    LAMBDA
      .New(this, "JsonViewer")
      .ReadsAppConfig(appConfig)
      .Export(ManifesterConfig.JSON_VIEWER);

    LAMBDA
      .New(this, "YamlViewer")
      .ReadsAppConfig(appConfig)
      .Export(ManifesterConfig.YAML_VIEWER);

  }
  
}
