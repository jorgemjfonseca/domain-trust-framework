import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../../Common/LAMBDA/LAMBDA';
import { BUS } from '../../../../Common/BUS/BUS';
import { DYNAMO } from '../../../../Common/DYNAMO/DYNAMO';
import { API } from '../../../../Common/API/API';
import { SharedComms } from '../../../../Behaviours/SharedComms/stack/SharedComms';
import { SyncApiBehaviour } from '../../../../Behaviours/SyncApi/stack/SyncApiBehaviour';
import { STACK } from '../../../../Common/STACK/STACK';

// https://quip.com/a167Ak79FKlt/-Issuer
export class IssuerActor extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, IssuerActor.name, props);

    const bus = BUS.Import(this, SharedComms.BUS);
    const router = API.Import(this, SyncApiBehaviour.ROUTER);

    const credentials = DYNAMO
      .New(this, 'Credentials');

    LAMBDA
      .New(this, 'DownloadHandlerFn')
      .AddApiMethod(router, 'Issuer-Download')
      .ReadsFromDynamoDB(credentials);

    LAMBDA
      .New(this, 'StatusHandlerFn')
      .SpeaksWithBus(bus, 'Issuer-Status')
      .ReadsFromDynamoDB(credentials);

  }
}
