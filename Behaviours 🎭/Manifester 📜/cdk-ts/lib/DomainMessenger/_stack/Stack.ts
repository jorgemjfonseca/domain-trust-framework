import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as events from 'aws-cdk-lib/aws-events';
import * as targets from 'aws-cdk-lib/aws-events-targets';
import { WAF, WebACLAssociation } from '../waf/Waf';
import * as kms from 'aws-cdk-lib/aws-kms';
import { API } from '../api/Api';
import { DLQ, QUEUE } from '../../Common/Queue/Queue';
import { LAMBDA } from '../../Common/Lambda/Lambda';

export class DomainMessenger extends cdk.Stack {
  constructor(scope: Construct, props?: cdk.StackProps) {
    super(scope, DomainMessenger.name, props);
   
    // SENDER LAMBDA
    const senderDlq = new DLQ(this, 'SenderDLQ');
    const senderLambda = new LAMBDA(this, "Sender", senderDlq, {
      runtime: lambda.Runtime.NODEJS_18_X,
      code: lambda.Code.fromAsset('lib/' + DomainMessenger.name + '/lambda/sender'),
      handler: 'exports.handler',
      memorySize: 1024, 
      timeout: cdk.Duration.seconds(30)
    });

    // SENDER QUEUE
    const senderQueue = new QUEUE(this, 'SenderQueue', senderDlq)
    senderLambda.ConsumeMessagesFrom(senderQueue);
    
    // WRAPPER FUNCTION
    const wrapperDlq = new DLQ(this, 'WrapperDLQ');
    const wrapperLambda = new LAMBDA(this, "Wrapper", wrapperDlq, {
      runtime: lambda.Runtime.NODEJS_18_X,
      code: lambda.Code.fromAsset('lib/' + DomainMessenger.name + '/lambda/wrapper'),
      handler: 'exports.handler',
      memorySize: 1024, 
      timeout: cdk.Duration.seconds(5),
      deadLetterQueue: wrapperDlq,
      environment: {
        QUEUE_NAME: senderQueue.queueName
      }
    });
    wrapperLambda.SendMessagesToQueue(senderQueue);

    // KMS
    // https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_kms.Key.html#alias
    new kms.Key(this, 'DomainMessengerKey', {
      alias: 'DomainMessengerKey',
      keySpec: kms.KeySpec.RSA_2048, 
      keyUsage: kms.KeyUsage.SIGN_VERIFY
    }).grantEncrypt(wrapperLambda);

    // EVENT BUS

    const bus = new events.EventBus(this, 'Bus', { 
      eventBusName: this.stackName+'Bus'});
    
    new events.Rule(this, 'wrapperLambda', {
      eventPattern: {
        source: ["DTFW"]
      },
      targets: [
        new targets.LambdaFunction(wrapperLambda, {
          deadLetterQueue: wrapperDlq,
          maxEventAge: cdk.Duration.hours(2),
          retryAttempts: 2,
        })
      ]
    });

    // CERTIFICATE MANAGER

    // API GATEWAY
    const receiverApi = new API(this, 'ReceiverApi');
    new cdk.CfnOutput(this, 'ReceiverApiId', {
      value: receiverApi.restApiId,
      exportName: 'ReceiverApiId',
    });

    // WAF
    new WAF(this, 'WAFv2')
      .Associate('DevAssociation', receiverApi.Arn());

    // RECEIVER QUEUE
    const receiverDlq = new DLQ(this, 'ReceiverDLQ');
    const receiverQueue = new QUEUE(this, 'ReceiverQueue', receiverDlq);
    receiverApi.SendMessagesTo(receiverQueue);

    // UNWRAPPER FUNCTION
    new LAMBDA(this, "Unwrapper", receiverDlq, {
      runtime: lambda.Runtime.NODEJS_18_X,
      code: lambda.Code.fromAsset('lib/' + DomainMessenger.name + '/lambda/wrapper'),
      handler: 'exports.handler',
      memorySize: 1024, 
      timeout: cdk.Duration.seconds(20)
    })
    .ConsumeMessagesFrom(receiverQueue)
    .SendMessagesToBus(bus);

  }
}

