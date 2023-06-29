import * as cdk from 'aws-cdk-lib';
import * as kms from 'aws-cdk-lib/aws-kms';
import * as iam from 'aws-cdk-lib/aws-iam';
import { STACK } from '../STACK/STACK';
import { CONSTRUCT } from '../CONSTRUCT/CONSTRUCT';

// https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_kms.Key.html#alias
export class KMS_KEY extends CONSTRUCT {

    Super: kms.Key;
    Alias: string;
    
    constructor(scope: STACK, sup: kms.Key, alias: string) {
      super(scope);
      this.Super = sup;
      this.Alias = alias;
    }

    private static New(scope: STACK, id: string, props: kms.KeyProps): KMS_KEY {
      const alias = scope.stackName + id;
      const sup = new kms.Key(scope, id, {
        alias: alias,
        removalPolicy: cdk.RemovalPolicy.DESTROY,
        enableKeyRotation: false,
        pendingWindow: cdk.Duration.days(7),
        ...props
      });

      const ret = new KMS_KEY(scope, sup, alias);
      return ret;
    }


    public static NewForDomain(scope: STACK, id: string): KMS_KEY {
        return KMS_KEY.New(scope, id, {
          keySpec: kms.KeySpec.RSA_2048,
          keyUsage: kms.KeyUsage.SIGN_VERIFY,
        });
    }
    

    public static NewForDnsSec(scope: STACK, id: string): KMS_KEY {
        const ret = KMS_KEY.New(scope, id, {
          keySpec: kms.KeySpec.ECC_NIST_P256,
          keyUsage: kms.KeyUsage.SIGN_VERIFY,
        });
        ret.GrantToDnsSec();
        return ret;
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
      
      return this;
    }

    public static ImportFromRegion(
      scope: STACK, 
      stackRegion: string, 
      stackName: string, 
      alias: string
    ): KMS_KEY {
      return new KMS_KEY(scope,
        kms.Key.fromKeyArn(scope, alias, 
          `arn:aws:kms:${stackRegion}:${cdk.Aws.ACCOUNT_ID}:alias/${stackName}${alias}`) as kms.Key,
        alias);
    }

    public static Import(scope: STACK, alias: string): KMS_KEY {
      return new KMS_KEY(scope,
        kms.Key.fromKeyArn(scope, alias, cdk.Fn.importValue(alias+'Arn')) as kms.Key,
        cdk.Fn.importValue(alias));
    }

    public GrantToDnsSec() {
      this.GrantToService('dnssec-route53.amazonaws.com');
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