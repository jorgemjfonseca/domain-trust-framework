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
      .HandlesSyncApi('Host-CheckIn');

    LAMBDA
      .New(this, "TalkerHandlerFn")
      .WritesToDynamoDB(sessions, 'SESSIONS')
      .HandlesMessenger('Host-Talker');

    LAMBDA
      .New(this, "CheckOutHandlerFn")
      .WritesToDynamoDB(sessions, 'SESSIONS')
      .HandlesMessenger('Host-CheckOut');

    LAMBDA
      .New(this, "AbandonedHandlerFn")
      .WritesToDynamoDB(sessions, 'SESSIONS')
      .HandlesMessenger('Host-Abandoned');

    LAMBDA
      .New(this, "DownloadHandlerFn")
      .ReadsFromDynamoDB(sessions, "SESSIONS")
      .ReadsFromDynamoDB(files, "FILES")
      .HandlesSyncApi('Host-Download');

    LAMBDA
      .New(this, "UploadHandlerFn")
      .ReadsFromDynamoDB(sessions, 'SESSIONS')
      .WritesToDynamoDB(files, 'FILES')
      .HandlesSyncApi('Host-Upload');

    LAMBDA
      .New(this, "FoundHandlerFn")
      .WritesToDynamoDB(sessions, 'SESSIONS')
      .HandlesMessenger('Host-Found');

  }
}
