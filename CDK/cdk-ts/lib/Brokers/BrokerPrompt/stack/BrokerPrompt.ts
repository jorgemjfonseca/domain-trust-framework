import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';


/** 👉 https://quip.com/FNbzAVSVu9z6#RCPABAYylHR */
export class BrokerPrompt extends STACK {

  public static New(scope: Construct, props?: cdk.StackProps): BrokerPrompt {
    const ret = new BrokerPrompt(scope, props);
    return ret;
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, BrokerPrompt.name, props);

    LAMBDA
      .New(this, 'Prompt')
      .HandlesMessenger('Prompt@Broker');

  }

}
