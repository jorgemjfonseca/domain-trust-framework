import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { DYNAMO } from '../../../../Common/DYNAMO/DYNAMO';
import { VaultActor as Vault } from '../../Vault/stack/VaultActor';
import { STACK } from '../../../../Common/STACK/STACK';

interface ProfileDependencies {
  vault: Vault
}

// https://quip.com/SEI9ASIzc2C5/-Profile
export class Profile extends STACK {

  private Dependencies: ProfileDependencies;

  public static New(scope: Construct, deps: ProfileDependencies, props?: cdk.StackProps): Profile {
    const ret = new Profile(scope, deps, props);
    ret.addDependency(deps.vault);
    ret.Dependencies = deps;
    return ret;
  }

  private constructor(scope: Construct, deps: ProfileDependencies, props?: cdk.StackProps) {
    super(scope, Profile.name, props);

    const userData = DYNAMO
      .New(this, 'UserData');

      /*
    deps.vault
      .GetDiscloseFn()
      .ReadsFromDynamoDB(userData, 'USERDATA');
      */

  }
}
