import * as cdk from 'aws-cdk-lib';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import { STACK } from '../STACK/STACK';
import { CONSTRUCT } from '../CONSTRUCT/CONSTRUCT';


export class SECRET extends CONSTRUCT {

    Super: secretsmanager.Secret;    

    public static NewString(
      scope: STACK, 
      value: string
    ): SECRET {

        const ret = new SECRET(scope);

        ret.Super = new secretsmanager.Secret(ret, 'Secret', { 
          secretStringValue: cdk.SecretValue.unsafePlainText(value)
        });

        ret.Scope = scope;

        return ret;
    }
    
}