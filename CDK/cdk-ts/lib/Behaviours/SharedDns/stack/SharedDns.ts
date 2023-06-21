import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { ROUTE53 } from '../../../Common/ROUTE53/ROUTE53';
import { CERTIFICATE } from '../../../Common/CERTIFICATE/CERTIFICATE';
import { SharedComms } from '../../SharedComms/stack/SharedComms';
import { STACK } from '../../../Common/STACK/STACK';
import { KMS_KEY } from '../../../Common/KEY/KMS_KEY';
import { EC2_KEY } from '../../../Common/KEY/EC2_KEY';
import { CUSTOM } from '../../../Common/CUSTOM/CUSTOM';
import { LAMBDA } from '../../../Common/LAMBDA/LAMBDA';

export class SharedDns extends STACK {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, SharedDns.name, props);
    
    const domainName = this.Import(SharedComms.DOMAIN_NAME);
    const key = KMS_KEY.Import(this, SharedComms.SIGNATURE_KEY);

    const dns = ROUTE53
      .New(this, 'DNS', domainName)
      .AddTxtRecord(`dtfw._domainkey.${domainName}`, `k=rsa;p=?;`);

    const setDKIM = LAMBDA
      .New(this, 'SetDKIM', {
        runtime: LAMBDA.PYTHON_3_10,
        handler: 'index.on_event'
      })
      .GrantRoute53FullAccess()
      .GrantCloudFormationReadOnlyAccess()
      .GrantKeyManagementServicePowerUser();

    CUSTOM.New(setDKIM, 'Custom3');

    CERTIFICATE.NewByDns(this, "Certificate", dns);
    
  }
}
