import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { DomainDns } from '../../DomainDns/stack/DomainDns';
import { NODEJS } from '../../../Common/NODEJS/NODEJS';
import { DomainName } from '../../DomainName/stack/DomainName';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { ROUTE53 } from '../../../Common/ROUTE53/ROUTE53';
import { CUSTOM } from '../../../Common/CUSTOM/CUSTOM';


// 👉 https://quip.com/RnO6Ad0BuBSx/-Sync-API
export class SyncApiDkim extends STACK {

  public static readonly SIGNER_FN = 'SyncApiDkim-Signer';
  public static readonly VALIDATOR_FN = 'SyncApiDkim-Validator';

  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, SyncApiDkim.name, {
      description: 'Creates Key-Pair, sets DKIM.',
      ...props
    });

    // DEPENDENCIES
    const domainName = DomainName.GetDomainName(this);
    const dns = ROUTE53.ImportFromAlias(this, DomainDns.HOSTED_ZONE);

    // BLOCKS
    this.SetUpDkim(domainName, dns);
    this.SetUpSigner(domainName);
    this.SetUpValidator(domainName);
  }



  private SetUpDkim(domainName: string, dns: ROUTE53) {

    const dkimRecordName = `dtfw._domainkey.${domainName}`

    const dkimSetterFn = LAMBDA
      .New(this, 'DkimSetterFn', {
        runtime: LAMBDA.PYTHON_3_10,
        handler: 'index.on_event'
      })
      .GrantRoute53FullAccess();

    CUSTOM
      .New('Custom', dkimSetterFn, {
        domainName: domainName,
        hostedZoneId: dns.Super.hostedZoneId,
        hostedZoneNameServers: dns.Super.hostedZoneNameServers,
        dkimRecordName: dkimRecordName
      });

  }


  private SetUpSigner(domainName: string) {

    NODEJS
      .New(this, 'SignerFn', {})
      .Export(SyncApiDkim.SIGNER_FN)
      .AddEnvironment('DOMAIN_NAME', domainName);

  }


  private SetUpValidator(domainName: string) {
          
    NODEJS
      .New(this, 'DkimReaderFn');

    NODEJS
      .New(this, 'ValidatorFn')
      .Export(SyncApiDkim.VALIDATOR_FN)
      .AddEnvironment('DOMAIN_NAME', domainName);

  }



}
