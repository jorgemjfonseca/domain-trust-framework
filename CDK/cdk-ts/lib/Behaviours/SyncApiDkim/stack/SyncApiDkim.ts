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
  public static readonly DKIM_READER_FN = 'SyncApiDkim-DkimReader';

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

    const keyPairGenerator = NODEJS
      .New(this, 'KeyPairGeneratorFn');

    const secretSetterFn = LAMBDA
      .New(this, 'SecretSetterFn')
      .GrantSecretsManagerReadWrite();

    const dkimSetterFn = LAMBDA
      .New(this, 'DkimSetterFn')
      .GrantRoute53FullAccess()
      .AddEnvironment('dkimRecordName', `dtfw._domainkey.${domainName}`)
      .AddEnvironment('hostedZoneId', dns.Super.hostedZoneId);

    const keyPairRotatorFn = LAMBDA
      .New(this, 'KeyPairRotatorFn')
      .GrantLambdaInvocation()
      .AddEnvironment('KeyPairGeneratorFn', keyPairGenerator.FunctionName())
      .AddEnvironment('SecretSetterFn', secretSetterFn.FunctionName())
      .AddEnvironment('DkimSetterFn', dkimSetterFn.FunctionName());

    const cfnFn = LAMBDA
      .New(this, 'CfnFn', {
        runtime: LAMBDA.PYTHON_3_10,
        handler: 'index.on_event'
      })
      .GrantLambdaInvocation()
      .AddEnvironment('KeyPairRotatorFn', keyPairRotatorFn.FunctionName());

    CUSTOM.New('Custom', cfnFn);
  }


  private SetUpSigner(domainName: string) {

    NODEJS
      .New(this, 'SignerFn', {})
      .Export(SyncApiDkim.SIGNER_FN)
      .AddEnvironment('DOMAIN_NAME', domainName);

  }


  private SetUpValidator(domainName: string) {
          
    NODEJS
      .New(this, 'DkimReaderFn')
      .Export(SyncApiDkim.DKIM_READER_FN);

    NODEJS
      .New(this, 'ValidatorFn')
      .Export(SyncApiDkim.VALIDATOR_FN)
      .AddEnvironment('DOMAIN_NAME', domainName);

  }



}
