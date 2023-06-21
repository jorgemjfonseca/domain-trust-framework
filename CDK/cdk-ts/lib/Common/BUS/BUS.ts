import * as cdk from 'aws-cdk-lib';
import * as events from 'aws-cdk-lib/aws-events';
import { STACK } from '../STACK/STACK';
import { CONSTRUCT } from '../CONSTRUCT/CONSTRUCT';


export class BUS extends CONSTRUCT {

    Super: events.IEventBus;
    Name: string;

    constructor(scope: STACK, bus: events.IEventBus, name: string) {
      super(scope);
      this.Super = bus;
      this.Name = name;
    }

    public static New(scope: STACK, id: string = 'Bus', 
      props: cdk.aws_events.EventBusProps = {}
    ): BUS {
        
        const name = scope.Name + id;
        const sup = new events.EventBus(scope, id, {
          ...props,
          eventBusName: name
        });

        const ret = new BUS(scope, sup, name);
        return ret;
    }

    
    public Export(alias: string): BUS {
      new cdk.CfnOutput(this.Super, alias, {
        value: this.Super.eventBusName,
        exportName: alias,
      });
      return this;
    }


    public static Import(scope: STACK, alias: string): BUS {
      const name = cdk.Fn.importValue(alias);
      const sup = events.EventBus.fromEventBusName(scope, alias, name);
      const ret = new BUS(scope, sup, sup.eventBusName);
      return ret;
    }

}

