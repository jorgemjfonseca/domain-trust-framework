import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { BUS } from '../../../Common/BUS/BUS';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { SharedComms } from '../../SharedComms/stack/SharedComms';
import { SyncApiBehaviour } from '../../SyncApi/stack/SyncApiBehaviour';
import { API } from '../../../Common/API/API';
import { STACK } from '../../../Common/STACK/STACK';

// https://quip.com/s9oCAO3UR38A/-Host
export class HostBehaviour extends STACK {

  public static readonly SESSIONS = 'Host.SessionsTable';


  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, HostBehaviour.name, props);

    const bus = BUS.Import(this, SharedComms.BUS);
    const router = API.Import(this, SyncApiBehaviour.ROUTER);

    const sessions = DYNAMO
      .New(this, 'Sessions')
      .Export(HostBehaviour.SESSIONS);

    const files = DYNAMO
      .New(this, 'Files');

    LAMBDA
      .New(this, "CheckInHandlerFn")
      .AddApiMethod(router, 'Host-CheckIn')
      .WritesToDynamoDB(sessions);

    LAMBDA
      .New(this, "TalkerHandlerFn")
      .SpeaksWithBus(bus, 'Host-Talker')
      .WritesToDynamoDB(sessions);

    LAMBDA
      .New(this, "CheckOutHandlerFn")
      .SpeaksWithBus(bus, 'Host-CheckOut')
      .WritesToDynamoDB(sessions);

    LAMBDA
      .New(this, "AbandonedHandlerFn")
      .SpeaksWithBus(bus, 'Host-Abandoned')
      .WritesToDynamoDB(sessions);

    LAMBDA
      .New(this, "DownloadHandlerFn")
      .AddApiMethod(router, 'Host-Download')
      .ReadsFromDynamoDBs([ sessions, files ]);

    LAMBDA
      .New(this, "UploadHandlerFn")
      .AddApiMethod(router, 'Host-Upload')
      .ReadsFromDynamoDB(sessions)
      .WritesToDynamoDB(files);

    LAMBDA
      .New(this, "FoundHandlerFn")
      .SpeaksWithBus(bus, 'Host-Found')
      .WritesToDynamoDB(sessions);

  }
}
