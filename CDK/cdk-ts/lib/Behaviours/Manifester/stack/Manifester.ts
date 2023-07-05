import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { ManifesterAlerter } from '../../ManifesterAlerter/stack/ManifesterAlerter';
import { ManifesterConfig } from '../../ManifesterConfig/stack/ManifesterConfig';
import { SyncApi } from '../../SyncApi/stack/SyncApi';


export interface ManifesterDependencies {
  manifesterBucket: ManifesterConfig,
  manifesterAlerter: ManifesterAlerter,
  syncApi: SyncApi
}

/** 👉 https://quip.com/BfbEAAFo5aOV/-Manifester */
export class Manifester extends STACK {


  public static New(scope: Construct, deps: ManifesterDependencies): Manifester {
    const ret = new Manifester(scope);
    ret.addDependency(deps.manifesterBucket);
    ret.addDependency(deps.manifesterAlerter);
    ret.addDependency(deps.syncApi);
    return ret;
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, Manifester.name, {
      description: 'Manifester umbrella.',
      ...props
    });
  }

}
