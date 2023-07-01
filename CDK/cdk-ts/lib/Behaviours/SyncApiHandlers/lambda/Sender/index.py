# 📚 SyncApiHandlers-SenderFn

import os


# 👉️ https://hands-on.cloud/boto3-kms-tutorial/
# REQUEST { privateKey, publicKey, text }
# RESPONSE { hash, signature, isVerified }
def sign(privateKey: str, publicKey, text) -> str:
    from LAMBDA import LAMBDA
    return LAMBDA('SIGNER_FN').Invoke({
        'privateKey': privateKey,
        'publicKey': publicKey,
        'text': text
    })
    

def get_keys(): 
    from SECRETS import SECRETS
    return {
        'publicKey': SECRETS.Get('/dtfw/publicKey'),
        'privateKey': SECRETS.Get('/dtfw/privateKey')
    }


def wrap_envelope(message: any):
    from UTILS import UTILS

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
    from UTILS import UTILS

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
    from WEB import WEB
    from MSG import MSG

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