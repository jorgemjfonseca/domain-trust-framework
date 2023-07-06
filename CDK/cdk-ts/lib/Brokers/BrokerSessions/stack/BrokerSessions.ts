import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { DYNAMO } from '../../../Common/DYNAMO/DYNAMO';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';


/** 👉 https://quip.com/HrgkAuQCqBez#bXDABAe5brB */
export class BrokerSessions extends STACK {

  public static New(scope: Construct, props?: cdk.StackProps): BrokerSessions {
    const ret = new BrokerSessions(scope, props);
    return ret;
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, BrokerSessions.name, props);

    const hosts = DYNAMO.New(this, 'Hosts', { filtered: true });
    const sessions = DYNAMO.New(this, 'Sessions', { filtered: true });

    LAMBDA
      .New(this, 'Sessions')
      .ReadsFromDynamoDB(hosts, 'HOSTS')
      .ReadsFromDynamoDB(sessions, 'SESSIONS')
      .HandlesSyncApi('Sessions@Broker')

    LAMBDA
      .New(this, 'Talker')
      .HandlesMessenger('Talker@Broker');

    LAMBDA
      .New(this, 'Checkout')
      .HandlesMessenger('Checkout@Broker');

    LAMBDA
      .New(this, 'Abandon')
      .HandlesMessenger('Abandon@Broker');

    LAMBDA
      .New(this, 'Assess')
      .HandlesSyncApi('Assess@Broker');

    LAMBDA
      .New(this, 'Goodbye')
      .HandlesMessenger('Goodbye@Broker');
  }

}
