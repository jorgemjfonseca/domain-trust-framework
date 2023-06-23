import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../../Common/STACK/STACK';

// https://quip.com/m63tAErikib8/-Recurrent
export class RecurrentActor extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, RecurrentActor.name, props);

  }
}
