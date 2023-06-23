import * as cdk from 'aws-cdk-lib';
import * as kms from 'aws-cdk-lib/aws-kms';
import * as iam from 'aws-cdk-lib/aws-iam';
import { STACK } from '../STACK/STACK';
import { CONSTRUCT } from '../CONSTRUCT/CONSTRUCT';

// https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_kms.Key.html#alias
export class KMS_KEY extends CONSTRUCT {

    Super: kms.Key;
    KeySpec: string;
    Alias: string;
    
    constructor(scope: STACK, sup: kms.Key, spec: string, alias: string) {
      super(scope);
      this.Super = sup;
      this.KeySpec = spec;
      this.Alias = alias;
    }

    private static New(scope: STACK, id: string, spec:kms.KeySpec): KMS_KEY {
      const alias = scope.stackName + id;
      const sup = new kms.Key(scope, id, {
        alias: alias,
        keySpec: spec,
        keyUsage: kms.KeyUsage.SIGN_VERIFY,
        removalPolicy: cdk.RemovalPolicy.DESTROY,
        enableKeyRotation: false,
      });

      const ret = new KMS_KEY(scope, sup, spec, alias);
      return ret;
    }


    public static NewForDomain(scope: STACK, id: string): KMS_KEY {
        return KMS_KEY.New(scope, id, kms.KeySpec.RSA_2048);
    }
    

    public static NewForDnsSec(scope: STACK, id: string): KMS_KEY {
        return KMS_KEY.New(scope, id, kms.KeySpec.ECC_NIST_P256);
    }


    public Export(alias: string): KMS_KEY {
      new cdk.CfnOutput(this.Super, alias+'Arn', {
        value: this.Super.keyArn,
        exportName: alias + 'Arn',
      });
      new cdk.CfnOutput(this.Super, alias+'Alias', {
        value: this.Alias,
        exportName: alias + 'Alias',
      });
      new cdk.CfnOutput(this.Super, alias+'Spec', {
        value: this.KeySpec,
        exportName: alias + 'Spec',
      });
      return this;
    }


    public static Import(scope: STACK, alias: string): KMS_KEY {
      return new KMS_KEY(scope,
        kms.Key.fromKeyArn(scope, alias, cdk.Fn.importValue(alias+'Arn')) as kms.Key,
        cdk.Fn.importValue(alias+'Spec'), 
        cdk.Fn.importValue(alias+'Alias'));
    }


    public GrantToService(service: string) {

      this.Super.addToResourcePolicy(new iam.PolicyStatement({
        sid: "Allow Service " + service,
        effect: iam.Effect.ALLOW,
        principals: [
          new iam.ServicePrincipal(service)
        ],
        actions: [
          "kms:DescribeKey",
          "kms:GetPublicKey",
          "kms:Sign"
        ],
        resources: ["*"],
        conditions: {
          "StringEquals": {
            "aws:SourceAccount": cdk.Aws.ACCOUNT_ID
          }
        }
      }));
      
      this.Super.addToResourcePolicy(new iam.PolicyStatement({
        sid: "Allow CreateGrant for " + service,
        effect: iam.Effect.ALLOW,
        principals: [
          new iam.ServicePrincipal(service)
        ],
        actions: [
          "kms:CreateGrant"
        ],
        resources: ["*"],
        conditions: {
          "StringEquals": {
            "aws:SourceAccount": cdk.Aws.ACCOUNT_ID
          },
          "Bool": {
            "kms:GrantIsForAWSResource": true
          }
        }
      }));

    }

}