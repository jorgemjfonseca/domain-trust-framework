# SyncApi.SenderFn

import boto3
from urllib import request, parse
import base64
from base64 import b64encode
from hashlib import sha256
import os
import json
import uuid
import datetime


kms = boto3.client('kms')
domainName = os.environ['DOMAIN_NAME']


# 👉️ https://hands-on.cloud/boto3-kms-tutorial/
def sign(message: str) -> str:
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
    
   
# 👉️ https://datagy.io/python-sha256/
# 👉️ https://debugging.works/blog/verify-dkim-signature/
def digest(canonicalized: str) -> str: 
    utf8 = canonicalized.encode('utf-8')
    digested = sha256(utf8)
    hexdigested = digested.hexdigest()
    print(f'{hexdigested=}')
    return hexdigested
    
    
# 👉️ https://bobbyhadz.com/blog/python-json-dumps-no-spaces
def canonicalize(object: any) -> str:
    canonicalized = json.dumps(object, separators=(',', ':'))
    print(f'{canonicalized=}')
    return canonicalized
    
    
# 👉️ https://stackoverflow.com/questions/36484184/python-make-a-post-request-using-python-3-urllib    
def post(envelope: any) -> any:
    print(f'{envelope=}')

    to = envelope['Header']['To']
    url = 'https://_dtfw.' + to
    print(f'{url=}')

    data = parse.urlencode(envelope).encode()
    req = request.Request(url=url, data=data)
    resp = request.urlopen(req)
    return resp


# 👉️ https://stackoverflow.com/questions/53676600/string-formatting-of-utcnow
def timestamp():
    timestamp = datetime.datetime.utcnow().isoformat() + 'Z'
    print(f'{timestamp=}')
    return timestamp


# 👉️ https://stackoverflow.com/questions/37049289/how-do-i-convert-a-python-uuid-into-a-string
def correlation():
    correlation = str(uuid.uuid4());
    print(f'{correlation=}')
    return correlation


# 👉️ https://quip.com/NiUhAQKbj7zi
def process(message: any): 
    print(f'{message=}')
    
    defaults = {
        'Header': {
            'Correlation': correlation(),
            'Timestamp': timestamp()
        },
        'Body': {}
    }
    print(f'{defaults=}')
    
    overrides = {
        'Header': {
            'Code': 'dtfw.org/msg', 
            'Version': '1',
            'From': domainName
        }
    }
    print(f'{overrides=}')

    # 👉️ https://stackoverflow.com/questions/14839528/merge-two-objects-in-python
    envelope = defaults
    envelope['Header'].update(message['Header']) 
    envelope['Header'].update(overrides['Header'])
    if 'Body' in message:
        envelope['Body'].update(message['Body']) 
    
    canonicalized = canonicalize(envelope)
    digested = digest(canonicalized)
    signature = sign(canonicalized)
    
    envelope.update({
        'Signature': signature,
        'Hash': digested
    })
    
    response = post(envelope)
    return response


def handler(event, context):
    print(f'{event=}')

    message = event
    return process(message)
    

'''
{ 
    "Header": {
        "To": "7b61af20-7518-4d5a-b7c0-eee17e54bf7a.dev.dtfw.org",
        "Subject": "AnyMethod"
    }
}
'''    