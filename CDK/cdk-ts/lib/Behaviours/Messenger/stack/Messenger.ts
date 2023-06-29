import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { BUS } from '../../../Common/BUS/BUS';
import { SyncApiHandlers } from '../../SyncApiHandlers/stack/SyncApiHandlers';
import { STACK } from '../../../Common/STACK/STACK';
import { SyncApi } from '../../SyncApi/stack/SyncApi';


declare module '../../../Common/LAMBDA/LAMBDA' {
  interface LAMBDA {
    HandlesMessenger(action: string): LAMBDA;
    PublishesToMessenger(): LAMBDA;
  }
}

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
    const senderSync = LAMBDA
      .Import(this, SyncApiHandlers.SENDER);
    const receierSync = LAMBDA
      .Import(this, SyncApiHandlers.RECEIVER);
  
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


  private static BusCache: BUS;
  public static Bus(scope: STACK) {
    if (this.BusCache == null)
      this.BusCache = BUS
        .Import(scope, Messenger.BUS_NAME);
    return this.BusCache;
  }


  // EXTENSION
  public static HandlesMessenger(scope: STACK, action: string, lambda: LAMBDA): LAMBDA {
    
    // Receive all messages for this action from the API, and sends to the bus.
    const publisher = LAMBDA
      .Import(scope, Messenger.PUBLISHER);
    publisher.HandlesSyncApi(action);

    // Receives all messages from this action from the Bus.
    const bus = Messenger.Bus(scope);
    lambda.SpeaksWithBus(bus, action);
    return lambda;
  }


  // EXTENSION
  public static PublishesToMessenger(scope: STACK, lambda: LAMBDA): LAMBDA {
    const bus = Messenger.Bus(scope);
    lambda.PublishesToBus(bus);
    return lambda;
  }

}

