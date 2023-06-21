import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'cdk-ec2-key-pair';
import { STACK } from '../STACK/STACK';
import { CONSTRUCT } from '../CONSTRUCT/CONSTRUCT';

// https://pypi.org/project/cdk-ec2-key-pair/
// https://docs.aws.amazon.com/cdk/api/v1/docs/@aws-cdk_aws-ec2.CfnKeyPair.html
export class EC2_KEY extends CONSTRUCT {

    Super: ec2.KeyPair;
    Alias: string;
    
    constructor(scope: STACK, sup: ec2.KeyPair, alias: string) {
      super(scope);
      this.Super = sup;
      this.Alias = alias;
    }

    public static New(scope: STACK, id: string): EC2_KEY {
      const alias = scope.stackName + id;
      const sup = new ec2.KeyPair(scope, id, {
        name: alias,
        exposePublicKey: true,
        storePublicKey: true,
        publicKeyFormat: ec2.PublicKeyFormat.PEM
      });

      const ret = new EC2_KEY(scope, sup, alias);
      return ret;
    }

   
    public Export(alias: string): EC2_KEY {
      new cdk.CfnOutput(this.Super, alias, {
        value: this.Super.keyPairName,
        exportName: alias,
      });
      return this;
    }


}