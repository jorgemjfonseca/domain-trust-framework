import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { STACK } from '../../../Common/STACK/STACK';
import { DomainDns } from '../../DomainDns/stack/DomainDns';
import { NODEJS } from '../../../Common/NODEJS/NODEJS';
import { DomainName } from '../../DomainName/stack/DomainName';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';
import { ROUTE53 } from '../../../Common/ROUTE53/ROUTE53';
import { CUSTOM } from '../../../Common/CUSTOM/CUSTOM';


export interface SyncApiDkimDependencies {
  domainDns: DomainDns
}

// 👉 https://quip.com/RnO6Ad0BuBSx/-Sync-API
export class SyncApiDkim extends STACK {

  private static readonly SIGNER_FN = 'SyncApiDkim-Signer';
  private static readonly VALIDATOR_FN = 'SyncApiDkim-Validator';
  private static readonly DKIM_READER_FN = 'SyncApiDkim-DkimReader';

  public static GetValidator(scope: STACK) {
    return LAMBDA.Import(scope, SyncApiDkim.VALIDATOR_FN);
  }

  public static GetReader(scope: STACK) {
    return LAMBDA.Import(scope, SyncApiDkim.DKIM_READER_FN);
  }

  public static New(scope: Construct, deps: SyncApiDkimDependencies): SyncApiDkim {
    const ret = new SyncApiDkim(scope);
    ret.addDependency(deps.domainDns);
    return ret;
  }

  private constructor(scope: Construct, props?: cdk.StackProps) {
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
      .InvokesLambda(keyPairGenerator, 'KeyPairGeneratorFn')
      .InvokesLambda(secretSetterFn, 'SecretSetterFn')
      .InvokesLambda(dkimSetterFn, 'DkimSetterFn');

    const cfnFn = LAMBDA
      .New(this, 'CfnFn', {
        runtime: LAMBDA.PYTHON_3_10,
        handler: 'index.on_event'
      })
      .InvokesLambda(keyPairRotatorFn, 'KeyPairRotatorFn');

    CUSTOM
      .New('Custom', cfnFn);
  }

  public static GetSigner(stack: STACK): LAMBDA {
    return LAMBDA.Import(stack, SyncApiDkim.SIGNER_FN);
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

    const validator = NODEJS
      .New(this, 'ValidatorFn')
      .Export(SyncApiDkim.VALIDATOR_FN)
      .AddEnvironment('DOMAIN_NAME', domainName);

    // REGISTER EXTENSION
    LAMBDA
      .prototype
      .VerifiesSignatures = function() {
        this.InvokesLambda(validator);
        return this;
      };
  }

}


declare module '../../../Common/LAMBDA/LAMBDA' {
  interface LAMBDA {

    VerifiesSignatures(): LAMBDA;

  }
}