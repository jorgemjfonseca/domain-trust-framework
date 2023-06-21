import { STACK } from '../STACK/STACK';
import { CONSTRUCT } from '../CONSTRUCT/CONSTRUCT';
import * as custom from 'aws-cdk-lib/custom-resources';
import { LAMBDA } from '../LAMBDA/LAMBDA';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as logs from 'aws-cdk-lib/aws-logs';


// 
export class CUSTOM extends CONSTRUCT {

    Super: custom.Provider;
    
    constructor(scope: STACK) {
      super(scope);
    }

    public static New(
        onEventHandler: LAMBDA,
        id?: string
    ): CUSTOM {
        const scope = onEventHandler.Scope;
        const ret = new CUSTOM(scope);

        ret.Super = new custom.Provider(
          scope, 
          id ?? scope.RandomName('Custom'), 
          {
            onEventHandler: onEventHandler.Super,
            logRetention: logs.RetentionDays.ONE_DAY,
            //role
          });
 
        return ret;
    }
    
}