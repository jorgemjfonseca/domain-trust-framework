# SyncApiDkim-KeyPairRotatorFn

# 👉 https://medium.com/cyberark-engineering/advanced-custom-resources-with-aws-cdk-1e024d4fb2fa

import boto3
import json
import os
    

# 👉 https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/client/invoke.html
lambdaClient = boto3.client('lambda')
def invoke(functionName, params={}):
    print(f'invoking [{functionName}]({params})...')
    
    response = lambdaClient.invoke(
        FunctionName = functionName,
        Payload=json.dumps(params),
        LogType='Tail')
        
    print({
        'StatusCode': response["StatusCode"]
    })
    if response['StatusCode'] != 200:
        raise Exception(response['Payload'].read())
        
    ret = json.loads(response['Payload'].read())
    return ret


def handler(event, context):
    
    # Get the keys
    keys = invoke(os.environ['KeyPairGeneratorFn'])
    print(f'{keys=}')

    # Set Route53 DKIM with public key
    invoke(os.environ['DkimSetterFn'], {
        'public_key': keys['publicKey']
    })

    # Store the key pair in Secrets Manager
    invoke(os.environ['SecretSetterFn'], keys)