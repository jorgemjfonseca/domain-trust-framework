import * as cdk from 'aws-cdk-lib';
import * as neptune from '@aws-cdk/aws-neptune-alpha';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import { STACK } from '../STACK/STACK';

//https://github.com/amazon-archives/fully-automated-neo4j-to-neptune/blob/master/bootstrapper/lib/neptune-stack.js
export class NEPTUNE {

    Scope: STACK;
    Super: neptune.DatabaseCluster;
    
    public static New(
      scope: STACK, 
      id: string
    ): NEPTUNE {

        const ret = new NEPTUNE();

        const vpc = new ec2.Vpc(scope, "vpc", {
          natGateways: 0,
          subnetConfiguration: [
            {
              cidrMask: 24,
              name: "public",
              subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS
            }
          ]
        });

        const instanceSg = new ec2.SecurityGroup(scope, "instance-sg", {
          vpc: vpc,
          allowAllOutbound: true
        });
        instanceSg.addIngressRule(
          ec2.Peer.anyIpv4(),
          new ec2.Port({
            protocol: ec2.Protocol.TCP,
            stringRepresentation: "neo4j console",
            fromPort: 7474,
            toPort: 7474
          })
        );
        instanceSg.addIngressRule(
          ec2.Peer.anyIpv4(),
          new ec2.Port({
            protocol: ec2.Protocol.TCP,
            stringRepresentation: "neo4j bolt",
            fromPort: 7687,
            toPort: 7687
          })
        );
        instanceSg.addIngressRule(
          ec2.Peer.anyIpv4(),
          new ec2.Port({
            protocol: ec2.Protocol.TCP,
            stringRepresentation: "ssh",
            fromPort: 22,
            toPort: 22
          })
        );
    

        const sg = new ec2.SecurityGroup(scope, "neptune-sg", {
          vpc: vpc,
          allowAllOutbound: true
        });
        sg.connections.allowFrom(
          instanceSg,
          ec2.Port.allTcp(),
          "from ec2"
        );

        ret.Super = new neptune.DatabaseCluster(scope, id, { 
          vpc,
          instanceType: neptune.InstanceType.R5_LARGE,
        });

        return ret;
    }
    
}

