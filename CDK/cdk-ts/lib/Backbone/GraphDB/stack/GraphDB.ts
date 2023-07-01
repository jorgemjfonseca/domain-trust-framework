import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { NEPTUNE } from '../../../Common/NEPTUNE/NEPTUNE';
import { STACK } from '../../../Common/STACK/STACK';

// https://quip.com/hgz4A3clvOes/-Graph
export class GraphDB extends STACK {

  public static readonly NEPTUNE_HOSTNAME = "NeptuneHostname";
  public static readonly NEPTUNE_PORT = "NeptunePort";

  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, GraphDB.name, { 
      description: 'Creates the Neptune DB.',
      ...props
    });

    const neptune = NEPTUNE
      .New(this, 'Neptune');

    this.Export(
      GraphDB.NEPTUNE_HOSTNAME, 
      neptune.Super.clusterEndpoint.hostname);
      
    this.Export(
      GraphDB.NEPTUNE_PORT, 
      neptune.Super.clusterEndpoint.port.toString());
      
  }
}
