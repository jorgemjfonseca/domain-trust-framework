# 

import boto3
from urllib import request, parse
import base64
import os

kms = boto3.client('kms')


# https://hands-on.cloud/boto3-kms-tutorial/
def sign(message):
    print(f'{message=}')

    keyId = os.environ['KEY_ARN']
    print(f'{keyId=}')

    response = kms.sign(
        KeyId=keyId,
        Message=message,
        MessageType='RAW',
        GrantTokens=['string'],
        SigningAlgorithm='RSASSA_PSS_SHA_256'
    )

    bytes = response['Signature']
    signature = base64.b64encode(bytes).decode()   

    print(f'{signature=}')
    return signature
   
    
def send(domain, envelope):
    print(f'{domain=}')
    print(f'{envelope=}')

    url = 'https://_dtfw.' + domain
    print(f'{url=}')
    
    data = parse.urlencode(envelope).encode()
    req = request.Request(url=url, data=data)
    resp = request.urlopen(req)
    return resp


def sign_and_send(domain, message): 
    print(f'{domain=}')
    print(f'{message=}')

    signature = sign(message);
    envelope = {
        message,
        signature
    }
    return send(domain, envelope)


def handler(event):
    print(f'{event=}')

    message = ''
    domain = '';
    return send(domain, message)
    