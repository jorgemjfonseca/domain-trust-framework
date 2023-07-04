import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { Manifester } from '../../Manifester/stack/Manifester';
import { Messenger } from '../../Messenger/stack/Messenger';
import { SyncApi } from '../../SyncApi/stack/SyncApi';

export interface DomainDependencies {
  manifester: Manifester,
  syncApi: SyncApi,
  messenger: Messenger
};

export class Domain extends STACK {
  
  public static New(scope: Construct, deps: DomainDependencies): Domain {
    const ret = new Domain(scope);
    ret.addDependency(deps.manifester);
    ret.addDependency(deps.syncApi);
    ret.addDependency(deps.messenger);
    return ret;
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, Domain.name, { 
      description: 'Full independent domain.',
      ...props
    });
    
  }

}
