import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { STACK } from '../../../Common/STACK/STACK';
import { Domain } from '../../Domain/stack/Domain';


export interface HostDependencies {
  domain: Domain
}


/** 👉 https://quip.com/s9oCAO3UR38A/-Host */
export class Host extends STACK {

  public static readonly SESSIONS = 'Host-SessionsTable';


  public static New(scope: Construct, deps: HostDependencies, props?: cdk.StackProps): Host {
    const ret = new Host(scope, props);
    ret.addDependency(deps.domain);
    return ret;
  }


  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, Host.name, props);

    const sessions = DYNAMO
      .New(this, 'Sessions')
      .Export(Host.SESSIONS);

    const files = DYNAMO
      .New(this, 'Files');

    LAMBDA
      .New(this, "CheckIn")
      .WritesToDynamoDB(sessions, 'SESSIONS')
      .HandlesSyncApi('CheckIn@Host');

    LAMBDA
      .New(this, "Talker")
      .WritesToDynamoDB(sessions, 'SESSIONS')
      .HandlesMessenger('Talker@Host');

    LAMBDA
      .New(this, "CheckOut")
      .WritesToDynamoDB(sessions, 'SESSIONS')
      .HandlesMessenger('CheckOut@Host');

    LAMBDA
      .New(this, "Abandoned")
      .WritesToDynamoDB(sessions, 'SESSIONS')
      .HandlesMessenger('Abandoned@Host');

    LAMBDA
      .New(this, "Download")
      .ReadsFromDynamoDB(sessions, "SESSIONS")
      .ReadsFromDynamoDB(files, "FILES")
      .HandlesSyncApi('Download@Host');

    LAMBDA
      .New(this, "Upload")
      .ReadsFromDynamoDB(sessions, 'SESSIONS')
      .WritesToDynamoDB(files, 'FILES')
      .HandlesSyncApi('Upload@Host');

    LAMBDA
      .New(this, "Found")
      .WritesToDynamoDB(sessions, 'SESSIONS')
      .HandlesMessenger('Found@Host');

  }
}
