# 📚 SyncApi.SenderFn

import boto3
from urllib import request, parse
import base64
from base64 import b64encode
from hashlib import sha256
import os
import json
import uuid
import datetime



# 👉 https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/client/invoke.html
lambdaClient = boto3.client('lambda')
def invoke(functionName, params):
    print(f'invoking [{functionName}]({params})...')
    
    response = lambdaClient.invoke(
        FunctionName = functionName,
        Payload=json.dumps(params),
        LogType='Tail')
    
    returned = json.loads(response['Payload'].read())
    print(f'{returned=}')
    return returned


# 👉️ https://hands-on.cloud/boto3-kms-tutorial/
# REQUEST { privateKey, publicKey, text }
# RESPONSE { hash, signature, isVerified }
def sign(privateKey: str, publicKey, text) -> str:
    return invoke(os.environ['SIGNER_FN'], {
        'privateKey': privateKey,
        'publicKey': publicKey,
        'text': text
    })
    
    
# 👉️ https://bobbyhadz.com/blog/python-json-dumps-no-spaces
def canonicalize(object: any) -> str:
    canonicalized = json.dumps(object, separators=(',', ':'))
    print(f'{canonicalized=}')
    return canonicalized
    
    
# 👉️ https://stackoverflow.com/questions/36484184/python-make-a-post-request-using-python-3-urllib    
def post(url: str, body: any) -> any:
    print(f'{url=}')

    data = parse.urlencode(body).encode()
    req = request.Request(url=url, data=data)
    resp = request.urlopen(req)
    
    charset=resp.info().get_content_charset()
    if charset == None:
        charset = 'utf-8'
    content=resp.read().decode(charset)
    
    return content


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

secretsmanager = boto3.client('secretsmanager')
def get_keys(): 
    return {
        'publicKey': secretsmanager.get_secret_value(SecretId='/dtfw/publicKey')['SecretString'],
        'privateKey': secretsmanager.get_secret_value(SecretId='/dtfw/privateKey')['SecretString']
    }


def wrap_envelope(message: any):
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
            'From': os.environ['DOMAIN_NAME']
        }
    }
    print(f'{overrides=}')

    # 👉️ https://stackoverflow.com/questions/14839528/merge-two-objects-in-python
    envelope = defaults
    envelope['Header'].update(message['Header']) 
    envelope['Header'].update(overrides['Header'])
    if 'Body' in message:
        envelope['Body'].update(message['Body']) 

    return envelope


def sign_envelope(envelope: any):
    keys = get_keys()
    canonicalized = canonicalize(envelope)
    signed = sign(keys['privateKey'], keys['publicKey'], canonicalized)

    if not signed['isVerified']:
        raise Exception('The sending signature is not valid!')
    
    envelope.update({
        'Signature': signed['signature'],
        'Hash': signed['hash']
    })
    return envelope


def send_envelope(envelope: any):
    to = envelope['Header']['To']
    url = f'https://dtfw.{to}/inbox'
    
    response = post(url, envelope)
    return response

   

# 👉️ https://quip.com/NiUhAQKbj7zi
def handler(event, context):
    print(f'{event=}')

    message = event
    envelope = wrap_envelope(message)
    envelope = sign_envelope(envelope)
    sent = send_envelope(envelope)
    return sent
    

'''
{ 
    "Header": {
        "To": "7b61af20-7518-4d5a-b7c0-eee17e54bf7a.dev.dtfw.org",
        "Subject": "AnyMethod"
    }
}
'''    