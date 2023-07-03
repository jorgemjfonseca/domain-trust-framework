import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { randomUUID } from 'crypto';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { CUSTOM } from '../../../Common/CUSTOM/CUSTOM';


export class DomainName extends STACK {
  
  private static readonly DOMAIN_NAME = 'DomainName';

  public static GetDomainName(scope: STACK): string {
    return scope.ImportSsm(DomainName.DOMAIN_NAME);
  }

  private SetDomainName() {
    const domainName = randomUUID() + '.dev.dtfw.org';
    
    const namerFn = LAMBDA
      .New(this, 'NamerFn', {
        runtime: LAMBDA.PYTHON_3_10,
        handler: 'index.on_event'
      })
      .GrantSsmFullAccess()
      .AddEnvironment('paramName', '/dtfw/' + DomainName.DOMAIN_NAME)
      .AddEnvironment('domainName', domainName);

    // Generate a new Random name, if one doesn't yet exist.
    // If it already exists, then ignore.
    CUSTOM.New('NamerFnRun', namerFn);

    this.ExportCfn('DomainName', domainName);
  }

  public static New(scope: Construct): DomainName {
    return new DomainName(scope);
  }
  
  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, DomainName.name, {
      description: 'Defines a random name for the domain.',
      ...props
    });

    this.SetDomainName();

  }

  

}
