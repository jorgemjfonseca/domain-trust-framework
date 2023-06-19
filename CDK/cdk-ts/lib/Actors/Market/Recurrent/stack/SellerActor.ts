import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../../Common/LAMBDA/LAMBDA';
import { BUS } from '../../../../Common/BUS/BUS';
import { DYNAMO } from '../../../../Common/DYNAMO/DYNAMO';
import { STACK } from '../../../../Common/STACK/STACK';

// https://quip.com/m63tAErikib8/-Recurrent
export class RecurrentActor extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, RecurrentActor.name, props);

  }
}
