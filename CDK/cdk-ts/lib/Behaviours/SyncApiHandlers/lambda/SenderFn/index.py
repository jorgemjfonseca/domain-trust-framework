# 📚 SyncApiHandlers-SenderFn

import os

from LAMBDA import LAMBDA
from UTILS import UTILS
from SECRETS import SECRETS
from MSG import MSG
from WEB import WEB


# 👉️ https://hands-on.cloud/boto3-kms-tutorial/
# REQUEST { privateKey, publicKey, text }
# RESPONSE { hash, signature, isVerified }
def sign(privateKey: str, publicKey, text) -> str:
    return LAMBDA('SIGNER_FN').Invoke({
        'privateKey': privateKey,
        'publicKey': publicKey,
        'text': text
    })
    

def get_keys(): 
    return {
        'publicKey': SECRETS.Get('/dtfw/publicKey'),
        'privateKey': SECRETS.Get('/dtfw/privateKey')
    }


def wrap_envelope(message: any):
    defaults = {
        'Header': {
            'Correlation': UTILS.Correlation(),
            'Timestamp': UTILS.Timestamp()
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
    canonicalized = UTILS.Canonicalize(envelope)
    signed = sign(keys['privateKey'], keys['publicKey'], canonicalized)

    if not signed['isVerified']:
        raise Exception('The sending signature is not valid!')
    
    envelope.update({
        'Signature': signed['signature'],
        'Hash': signed['hash']
    })
    return envelope


def send_envelope(envelope: any):
    to = MSG(envelope).To()
    url = f'https://dtfw.{to}/inbox'
    
    response = WEB.Post(url, envelope)
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