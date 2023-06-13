import * as cdk from 'aws-cdk-lib';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as kms from 'aws-cdk-lib/aws-kms';

// https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_kms.Key.html#alias
export class KEY  {

    Dlq: sqs.Queue;
    Super:  kms.Key;

    public static New(scope: cdk.Stack , id: string): KEY {
        const ret = new KEY();

        ret.Super = new  kms.Key(scope, id, {
          alias: scope.stackName + id,
          keySpec: kms.KeySpec.RSA_2048, 
          keyUsage: kms.KeyUsage.SIGN_VERIFY
        });
 
        return ret;
    }
    
}