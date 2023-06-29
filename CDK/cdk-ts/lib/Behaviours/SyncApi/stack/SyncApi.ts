import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { DomainDns } from '../../DomainDns/stack/DomainDns';
import { SyncApiDkim } from '../../SyncApiDkim/stack/SyncApiDkim';
import { SyncApiEndpoint } from '../../SyncApiEndpoint/stack/SyncApiEndpoint';
import { SyncApiHandlers } from '../../SyncApiHandlers/stack/SyncApiHandlers';

export interface SyncApiDependencies {
  domainDns: DomainDns,
  syncApiDkim: SyncApiDkim;
  syncApiEndpoint: SyncApiEndpoint;
  syncApiHandlers: SyncApiHandlers;
}

// 👉 https://quip.com/RnO6Ad0BuBSx/-Sync-API
export class SyncApi extends STACK {

  public static New(scope: Construct, deps: SyncApiDependencies): SyncApi {
    const ret = new SyncApi(scope);
    ret.addDependency(deps.domainDns);
    ret.addDependency(deps.syncApiDkim);
    ret.addDependency(deps.syncApiEndpoint);
    ret.addDependency(deps.syncApiHandlers);
    return ret;
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, SyncApi.name, {
      ...props,
      description: 'Sync API umbrella.'
    });

  }

}
