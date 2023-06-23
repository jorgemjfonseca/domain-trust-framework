import * as cdk from 'aws-cdk-lib';
import { STACK } from '../STACK/STACK';
import { CONSTRUCT } from '../CONSTRUCT/CONSTRUCT';
import * as custom from 'aws-cdk-lib/custom-resources';
import { LAMBDA } from '../LAMBDA/LAMBDA';
import * as logs from 'aws-cdk-lib/aws-logs';


// 
export class CUSTOM extends CONSTRUCT {

    Super: cdk.CustomResource;
    
    constructor(scope: STACK) {
      super(scope);
    }

    public static New(
        id: string,
        onEventHandler: LAMBDA,
        properties?: {
          [key: string]: any;
        }
    ): CUSTOM {
        const scope = onEventHandler.Scope;
        const ret = new CUSTOM(scope);

        const provider = new custom.Provider(
          scope, 
          id ?? scope.RandomName('Provider'), 
          {
            onEventHandler: onEventHandler.Super,
            logRetention: logs.RetentionDays.ONE_DAY,
            //role,
          });

        // https://github.com/aws/aws-cdk/issues/21058
        ret.Super = new cdk.CustomResource(
          scope, 
          scope.RandomName('CustomResource'), 
          { 
            serviceToken: provider.serviceToken,
            properties: properties
          });

        return ret;
    }
    
}