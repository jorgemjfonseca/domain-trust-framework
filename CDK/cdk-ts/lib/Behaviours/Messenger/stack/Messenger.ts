import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { BUS } from '../../../Common/BUS/BUS';
import { SyncApiHandlers } from '../../SyncApiHandlers/stack/SyncApiHandlers';
import { STACK } from '../../../Common/STACK/STACK';
import { SyncApi } from '../../SyncApi/stack/SyncApi';

export interface MessengerDependencies {
  syncApi: SyncApi
}


//https://quip.com/Fxj4AdnE6Eu5/-Messenger
export class Messenger extends STACK {

  private static readonly BUS_NAME = 'DtfwBus';
  private static readonly PUBLISHER = 'MessengerPublisher';

  public static New(scope: Construct, deps: MessengerDependencies): Messenger {
    const ret = new Messenger(scope);
    ret.addDependency(deps.syncApi);
    return ret;
  }
 
  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, Messenger.name, {
      description: 'Creates async message bus.',
      ...props
    });

    // IMPORTS
    const senderSync = SyncApiHandlers.GetSenderFn(this);
  
    // BUS
    const bus = BUS
      .New(this)
      .Export(Messenger.BUS_NAME);

    // SENDER FUNCTION 
    LAMBDA
      .New(this, "SenderFn")
      .InvokesLambda(senderSync, 'SENDER');

    // PUBLISHER FUNCTION
    LAMBDA.New(this, "PublisherFn")
      .PublishesToBus(bus)
      .Export(Messenger.PUBLISHER);

    // REGISTER EXTENSIONS
    LAMBDA.prototype.HandlesMessenger = function(action: string) {
      return Messenger.HandlesMessenger(this.Scope, action, this);
    };
    
    LAMBDA.prototype.PublishesToMessenger = function() {
      return Messenger.PublishesToMessenger(this.Scope, this);
    };
    
  }

  private static GetPublisher(scope: STACK): LAMBDA {
    return LAMBDA.Import(scope, Messenger.PUBLISHER);
  }

  private static BusCache: BUS;
  public static GetBus(scope: STACK) {
    if (this.BusCache == null)
      this.BusCache = BUS
        .Import(scope, Messenger.BUS_NAME);
    return this.BusCache;
  }


  // EXTENSION
  public static HandlesMessenger(scope: STACK, action: string, fn: LAMBDA): LAMBDA {
    
    // Receive all messages for this action from the API, and sends to the bus.
    Messenger
      .GetPublisher(scope)
      .HandlesSyncApi(action);

    // Receives all messages from this action from the Bus.
    Messenger
      .GetBus(scope)
      .SpeaksWithLambda(fn, action);

    return fn;
  }


  // EXTENSION
  public static PublishesToMessenger(scope: STACK, lambda: LAMBDA): LAMBDA {
    const bus = Messenger.GetBus(scope);
    lambda.PublishesToBus(bus);
    return lambda;
  }

}

declare module '../../../Common/LAMBDA/LAMBDA' {
  interface LAMBDA {
    HandlesMessenger(action: string): LAMBDA;
    PublishesToMessenger(): LAMBDA;
  }
}
