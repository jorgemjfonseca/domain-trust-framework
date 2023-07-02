import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { STACK } from '../../../Common/STACK/STACK';

// https://quip.com/s9oCAO3UR38A/-Host
export class HostBehaviour extends STACK {

  public static readonly SESSIONS = 'Host-SessionsTable';


  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, HostBehaviour.name, props);

    const sessions = DYNAMO
      .New(this, 'Sessions')
      .Export(HostBehaviour.SESSIONS);

    const files = DYNAMO
      .New(this, 'Files');

    LAMBDA
      .New(this, "CheckInHandlerFn")
      .WritesToDynamoDB(sessions, 'SESSIONS')
      .HandlesSyncApi('CheckIn@Host');

    LAMBDA
      .New(this, "TalkerHandlerFn")
      .WritesToDynamoDB(sessions, 'SESSIONS')
      .HandlesMessenger('Talker@Host');

    LAMBDA
      .New(this, "CheckOutHandlerFn")
      .WritesToDynamoDB(sessions, 'SESSIONS')
      .HandlesMessenger('CheckOut@Host');

    LAMBDA
      .New(this, "AbandonedHandlerFn")
      .WritesToDynamoDB(sessions, 'SESSIONS')
      .HandlesMessenger('Abandoned@Host');

    LAMBDA
      .New(this, "DownloadHandlerFn")
      .ReadsFromDynamoDB(sessions, "SESSIONS")
      .ReadsFromDynamoDB(files, "FILES")
      .HandlesSyncApi('Download@Host');

    LAMBDA
      .New(this, "UploadHandlerFn")
      .ReadsFromDynamoDB(sessions, 'SESSIONS')
      .WritesToDynamoDB(files, 'FILES')
      .HandlesSyncApi('Upload@Host');

    LAMBDA
      .New(this, "FoundHandlerFn")
      .WritesToDynamoDB(sessions, 'SESSIONS')
      .HandlesMessenger('Found@Host');

  }
}
