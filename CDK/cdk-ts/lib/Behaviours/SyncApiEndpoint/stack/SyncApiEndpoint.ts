import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { API } from '../../../Common/API/API';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { STACK } from '../../../Common/STACK/STACK';
import { WAF } from '../../../Common/WAF/WAF';
import { DomainDns } from '../../DomainDns/stack/DomainDns';
import { CERTIFICATE } from '../../../Common/CERTIFICATE/CERTIFICATE';
import { ROUTE53 } from '../../../Common/ROUTE53/ROUTE53';
import { CUSTOM } from '../../../Common/CUSTOM/CUSTOM';
import { DomainName } from '../../DomainName/stack/DomainName';
import { SyncApiHandlers } from '../../SyncApiHandlers/stack/SyncApiHandlers';

export interface SyncApiEndpointDependencies {
  domainDns: DomainDns,
  syncApiHandlers: SyncApiHandlers
}

// 👉 https://quip.com/RnO6Ad0BuBSx/-Sync-API
export class SyncApiEndpoint extends STACK {

  
  public static readonly API = 'SyncApi';

  public static New(scope: Construct, deps: SyncApiEndpointDependencies): SyncApiEndpoint {
    const ret = new SyncApiEndpoint(scope);
    ret.addDependency(deps.domainDns);
    ret.addDependency(deps.syncApiHandlers);
    return ret;
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, SyncApiEndpoint.name, {
      description: 'Creates ApiGW+WAF with custom domain.',
      ...props
    });

    // BLOCKS
    const api = this.SetUpApi()
    this.SetUpInbox(api);
    this.SetUpCustomDomain(api);
    this.SetUpFirewall(api);
  }




  private SetUpApi(): API {
    const api = API
      .New(this)
      .Export(SyncApiEndpoint.API);

    return api;
  }


  private SetUpInbox(api: API) {
    // All changes to the API must be done on the same stack
    // because CDK doesn't redeploy the API after an import.
    LAMBDA
      .Import(this, SyncApiHandlers.RECEIVER)
      .AddApiMethod(api, 'inbox', 'POST');
  }

  
  private SetUpFirewall(api: API) {
    const waf = WAF
      .New(this, 'WAFv2')
      .AssociateApi(api);
  }



  private SetUpCustomDomain(api: API) {

    const rootDomain = 
      //'105b4478-eaa5-4b73-b2a5-4da2c3c2dac0.dev.dtfw.org';
      DomainName.GetDomainName(this);
    
    const dns = ROUTE53
      //.ImportFromDomainName(this, rootDomain);
      .ImportFromAlias(this, DomainDns.HOSTED_ZONE)  

    const certificate = CERTIFICATE
      .Import(this, DomainDns.CERTIFICATE);
  

    // CAN'T SET APIGW IN ROUTE53 USING CDK WITH MULTIPLE STACKS, 
    //   SO SWITCHIN TO A CUSTOM CDK STEP INSTEAD.
    const domainName = api.AddCertificate('dtfw', rootDomain, certificate)
    this.Export('ApiAliasHostedZoneId', domainName.domainNameAliasHostedZoneId);
    this.Export('ApiAliasDomainName', domainName.domainNameAliasDomainName);
    this.Export('ApiDomainName', domainName.domainName);
    this.Export('ApiEndpoint', api.DefaultDomain())

    const setAliasFn = LAMBDA
      .New(this, 'SetAliasFn', {
        runtime: LAMBDA.PYTHON_3_10,
        handler: 'index.on_event'
      })
      .GrantRoute53FullAccess();
    
    CUSTOM
      .New('Custom', setAliasFn, {
        //apiEndpoint: api.DefaultDomain(), 
        apiDomain: domainName.domainName,
        apiHostedZoneId: domainName.domainNameAliasHostedZoneId,
        apiAlias: domainName.domainNameAliasDomainName,
        customDomain: 'dtfw.'+rootDomain,
        hostedZoneId: dns.Super.hostedZoneId,
      });
      
    // Test 👉 https://www.sslshopper.com/ssl-checker.html
    // Test 👉 https://www.digicert.com/help/
  }
  

}
