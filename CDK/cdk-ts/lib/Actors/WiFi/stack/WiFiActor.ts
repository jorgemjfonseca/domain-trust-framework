import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { STACK } from '../../../Common/STACK/STACK';

// https://quip.com/3HanAwD0KfJg/-Wi-Fi
export class WiFiActor extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, WiFiActor.name, props);
      
    LAMBDA
      .New(this, 'ConsumeHandlerFn')
      .HandlesSyncApi('WiFi-Consume');
  }
}
