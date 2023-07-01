# 📚 SyncApiHandlers-SenderFn

import boto3
from urllib import request, parse
import os
import json
import uuid
import datetime
import dtfw



# 👉️ https://hands-on.cloud/boto3-kms-tutorial/
# REQUEST { privateKey, publicKey, text }
# RESPONSE { hash, signature, isVerified }
def sign(privateKey: str, publicKey, text) -> str:
    return dtfw.LAMBDA('SIGNER_FN').Invoke({
        'privateKey': privateKey,
        'publicKey': publicKey,
        'text': text
    })
    


secretsmanager = boto3.client('secretsmanager')
def get_keys(): 
    return {
        'publicKey': secretsmanager.get_secret_value(SecretId='/dtfw/publicKey')['SecretString'],
        'privateKey': secretsmanager.get_secret_value(SecretId='/dtfw/privateKey')['SecretString']
    }


def wrap_envelope(message: any):
    defaults = {
        'Header': {
            'Correlation': dtfw.UTIL.Correlation(),
            'Timestamp': dtfw.UTIL.Timestamp()
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
    canonicalized = dtfw.UTILS.Canonicalize(envelope)
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
    
    response = dtfw.UTILS.Post(url, envelope)
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