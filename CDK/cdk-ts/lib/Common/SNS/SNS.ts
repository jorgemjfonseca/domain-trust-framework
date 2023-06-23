import * as cdk from 'aws-cdk-lib';
import * as sns from 'aws-cdk-lib/aws-sns';
import { STACK } from '../STACK/STACK';


export class SNS {

    Scope: STACK;
    Super: sns.Topic;
    

    public static New(
      scope: STACK , 
      id: string
    ): SNS {

        const ret = new SNS();

        ret.Super = new sns.Topic(scope, id,{ 
          topicName: `${scope.Name}-${id}`
        });

        ret.Scope = scope;

        return ret;
    }
    
}