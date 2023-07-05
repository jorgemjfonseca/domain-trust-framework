import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { Domain } from '../../../Behaviours/Domain/stack/Domain';
import { BrokerBinds } from '../../BrokerBinds/stack/BrokerBinds';
import { BrokerCredentials } from '../../BrokerCredentials/stack/BrokerCredentials';
import { BrokerPay } from '../../BrokerPay/stack/BrokerPay';
import { BrokerPrompt } from '../../BrokerPrompt/stack/BrokerPrompt';
import { BrokerSessions } from '../../BrokerSessions/stack/BrokerSessions';
import { BrokerSetup } from '../../BrokerSetup/stack/BrokerSetup';
import { BrokerShare } from '../../BrokerShare/stack/BrokerShare';


export interface BrokerDependencies {
  domain: Domain,
  brokerBinds: BrokerBinds,
  brokerCredentials: BrokerCredentials,
  brokerPay: BrokerPay,
  brokerPrompt: BrokerPrompt,
  brokerSessions: BrokerSessions,
  brokerSetup: BrokerSetup
  brokerShare: BrokerShare
}


/** 👉 https://quip.com/SJadAQ8syGP0/-Broker */
export class Broker extends STACK {

  public static New(scope: Construct, deps: BrokerDependencies, props?: cdk.StackProps): Broker {
    const ret = new Broker(scope, props);
    ret.addDependency(deps.domain);
    ret.addDependency(deps.brokerBinds);
    ret.addDependency(deps.brokerCredentials);
    ret.addDependency(deps.brokerPay);
    ret.addDependency(deps.brokerPrompt);
    ret.addDependency(deps.brokerSessions);
    ret.addDependency(deps.brokerSetup);
    ret.addDependency(deps.brokerShare);
    return ret;
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, Broker.name, props);

  }

}
