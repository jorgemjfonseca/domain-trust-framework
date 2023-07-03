import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { STACK } from '../../../Common/STACK/STACK';
import { Messenger } from '../../Messenger/stack/Messenger';
import { ManifesterConfig } from '../../ManifesterConfig/stack/ManifesterConfig';
import { APPCONFIG } from '../../../Common/APPCONFIG/APPCONFIG';
import { SQS } from '../../../Common/SQS/SQS';


export interface ManifesterAlerterDependencies {
  messenger: Messenger,
  manifesterBucket: ManifesterConfig
}

//https://quip.com/BfbEAAFo5aOV/-Manifester
export class ManifesterAlerter extends STACK {

  public static readonly BUCKET = 'DomainManifestBucket';

  public static New(scope: Construct, deps: ManifesterAlerterDependencies): ManifesterAlerter {
    const ret = new ManifesterAlerter(scope);
    ret.addDependency(deps.messenger);
    ret.addDependency(deps.manifesterBucket);
    return ret;
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, ManifesterAlerter.name, { 
      description: 'Alerts listeners on manifest changes.', 
      ...props 
    });

    const sqs = SQS.New(this, 'AlerterSqs');

    // ALERT LAMBDA
    LAMBDA.New(this, "Alerter")
      .TriggeredBySQS(sqs)
      .PublishesToMessenger();

    const configArn = ManifesterConfig.GetConfigArn();
    this.Export('ConfigArn', configArn);

    const extension = APPCONFIG.PublishToSQS(this, configArn, sqs)
    this.Export('AppConfigToSqs', extension.ref);
    
  }
}
