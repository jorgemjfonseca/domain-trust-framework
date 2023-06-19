import * as cdk from 'aws-cdk-lib';
import * as kms from 'aws-cdk-lib/aws-kms';
import * as iam from 'aws-cdk-lib/aws-iam';
import { STACK } from '../STACK/STACK';

// https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_kms.Key.html#alias
export class KEY  {

    Super: kms.Key;
    KeySpec: kms.KeySpec;
    Alias: string;
    

    private static New(scope: STACK, id: string, spec:kms.KeySpec): KEY {
      const alias = scope.stackName + id;
      const sup = new kms.Key(scope, id, {
        alias: alias,
        keySpec: spec,
        keyUsage: kms.KeyUsage.SIGN_VERIFY,
        removalPolicy: cdk.RemovalPolicy.DESTROY,
        enableKeyRotation: false,
      });

      const ret = new KEY();
      ret.Super = sup;
      ret.KeySpec = spec;
      ret.Alias = alias;
      return ret;
    }

    public static NewForDomain(scope: STACK, id: string): KEY {
        return KEY.New(scope, id, kms.KeySpec.RSA_2048);
    }

    public static NewForDnsSec(scope: STACK, id: string): KEY {
        return KEY.New(scope, id, kms.KeySpec.ECC_NIST_P256);
    }

    public ExportArn(alias: string): KEY {
      new cdk.CfnOutput(this.Super, alias, {
        value: this.Super.keyArn,
        exportName: alias,
      });
      return this;
    }

    public ExportKeySpec(alias: string): KEY {
      new cdk.CfnOutput(this.Super, alias, {
        value: kms.KeySpec.RSA_2048,
        exportName: alias,
      });
      return this;
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