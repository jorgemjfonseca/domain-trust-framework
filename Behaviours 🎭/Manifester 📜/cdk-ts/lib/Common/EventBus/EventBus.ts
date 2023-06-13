import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as events from 'aws-cdk-lib/aws-events';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as s3n from 'aws-cdk-lib/aws-s3-notifications'


export class BUS {

    Super: events.IEventBus;
    Scope: cdk.Stack;
    Name: string;

    constructor(scope: cdk.Stack, bus: events.IEventBus, name: string) {
      this.Scope = scope;
      this.Super = bus;
      this.Name = name;
    }

    public static New(scope: cdk.Stack, id: string = 'Bus', 
      props: cdk.aws_events.EventBusProps = {}
    ): BUS {
        
        const name = scope.stackName + id;
        const sup = new events.EventBus(scope, id, {
          ...props,
          eventBusName: name
        });

        const ret = new BUS(scope, sup, name);
        return ret;
    }

    
    public Export(alias: string) {
      new cdk.CfnOutput(this.Super, alias, {
        value: this.Super.eventBusName,
        exportName: alias,
      });
    }


    public static Import(scope: cdk.Stack, alias: string): BUS {
      const name = cdk.Fn.importValue(alias);
      const sup = events.EventBus.fromEventBusName(scope, alias, name);
      const ret = new BUS(scope, sup, sup.eventBusName);
      return ret;
    }

}

