import * as lambda from 'aws-cdk-lib/aws-lambda';
import { STACK } from '../STACK/STACK';
import { LAMBDA, LAMBDAparams } from '../LAMBDA/LAMBDA';




export class NODEJS extends LAMBDA {

  public static New(
    scope: STACK, 
    id: string, 
    props?: LAMBDAparams
  ): NODEJS {

    const ret = LAMBDA.New(scope, id, {
      ...props,
      runtime: lambda.Runtime.NODEJS_18_X
    });

    return ret;
  }
    
}

