# 📚 SyncApiHandlers-ReceiverFn

import os
import json

from DYNAMO import DYNAMO
from LAMBDA import LAMBDA
from MSG import MSG
from TIMER import TIMER
from UTILS import UTILS
from DOMAIN import DOMAIN


table = DYNAMO('TABLE')
    


# REQUEST { hostname }
# RESPONSE: str
def invokeDkimReader(envelope, checks):
    print(f'{TIMER.Elapsed()} Invoke dns.google...')

    domain = MSG(envelope).From()
    hostname = f'dtfw._domainkey.{domain}'
    checks.append(f'Valid domain?: {hostname}')
    
    d = DOMAIN(domain)
    d.GetGoogleDns()
    print(f'{TIMER.Elapsed()} Validate dns.google...')

    isDnsSec = d.IsDnsSec()
    checks.append(f'IsDnsSec?: {isDnsSec}')
    if not isDnsSec:
        raise Exception(f"Sender is not DNSSEC protected.")

    isDkimSetUp = d.IsDkimSetUp()
    checks.append(f'DKIM set?: {isDkimSetUp}')
    if not isDkimSetUp:
        raise Exception(f"Sender DKIM not found for dtfw.")
    
    hasPublicKey = d.HasPublicKey()
    checks.append(f'Public Key set?: {hasPublicKey}')
    if not hasPublicKey:
        raise Exception(f"Public key not found on sender DKIM.")
    
    return d.PublicKey()
    

def validateTo(envelope: any, checks):
    to = MSG(envelope).To().lower()
    me = os.environ['DOMAIN_NAME'].lower()

    if to != me:
        raise Exception(f'Wrong domain. Expected [{me}], but received [{to}]!')
    checks.append(f'For me?: {True}')


# REQUEST { text, publicKey, signature }
# RESPONSE { hash, isVerified }
def invokeValidator(text, publicKey, signature):
    print(f'{TIMER.Elapsed()} Invoking validator...')

    validator = LAMBDA('VALIDATOR_FN').Invoke({
        'text': text,
        'publicKey': publicKey,
        'signature': signature
    })
    print(f'{validator=}')
    return validator


def validateHash(envelope, validator, checks):
    expected = validator['hash']
    received = MSG(envelope).Hash()
    
    isHashValid = (expected == received)
    checks.append(f'Valid hash?: {isHashValid}')

    if not isHashValid:
        raise Exception(f'Wrong hash: expected [{expected}] but received [{received}]!')


def validateSignature(validator, checks):
    isVerified = validator['isVerified']
    checks.append(f'Valid signature?: {isVerified}')

    if not isVerified:
        raise Exception(f'Invalid signature!')


def validateHashAndSignature(envelope: any, checks, speed):
    print(f'{TIMER.Elapsed()} Validating signature...')
    
    started = TIMER.StartWatch()
    msg = MSG(envelope)
    signature = msg.Signature()
    text = msg.Canonicalize()
    publicKey = invokeDkimReader(envelope, checks)
    speed['Get DKIM over DNSSEC'] = TIMER.StopWatch(started)

    started = TIMER.StartWatch()
    validator = invokeValidator(text, publicKey, signature)
    validateHash(envelope, validator, checks)
    validateSignature(validator, checks)
    speed['Verify signature'] = TIMER.StopWatch(started)


def validate(envelope, speed):
    print(f'{TIMER.Elapsed()} Validating...')
    
    error = None
    checks = []
    
    try:
        MSG(envelope).ValidateHeader()
        validateTo(envelope, checks)
        validateHashAndSignature(envelope, checks, speed) 
    except Exception as e:
        if hasattr(e, 'message'):
            error = f'{e.message}'
        else:
            error = f'{e}'
    
    ret = {
        'Error': error,
        'Checks': checks
    }

    print(f'{ret=}')
    return ret


def execute(validation, envelope, speed):
    print(f'{TIMER.Elapsed()} Executing...')
    started = TIMER.StartWatch()

    if validation['Error']:
        ret = { 
            'Result': 'Ignored, invalid envelope!'
        }
        print(f'{ret=}')
        return ret

    msg = MSG(envelope)
    subject = msg.Subject()
    target = DYNAMO.Get(subject)
    
    answer = None 
    if (target):
        answer = LAMBDA(target['Target']).Invoke(envelope)

    ret = {
        'Result': 'Executed',
        'Target': target,
        'Answer': answer
    }    
    print(f'{ret=}')

    speed['Execute method'] = TIMER.StopWatch(started)
    return ret


def output(envelope, validation, execution, speed):
    print(f'{TIMER.Elapsed()} Building the output...')

    output = {}
    if execution != None and 'Answer' in execution:
        output = execution['Answer']

    output['Insights'] = {
        'Speed': speed,
        'Execution': execution,
        'Validation': validation,
        'Received': envelope
    }

    print ('Returning...')
    if validation['Error']:
        return UTILS.HttpResponse(400, output)
    return UTILS.HttpResponse(200, output)


def parse(event):
    envelope = {}
    if 'httpMethod' not in event:
        envelope = event
    elif 'body' in event and event['body'] != None:
        envelope = json.loads(event['body'])
    elif event['httpMethod'] == 'GET':
        envelope = {}

    return envelope 


def handler(event, context):
    print(f'{event=}')

    envelope = parse(event)
    print(f'{envelope=}')
    if envelope == {}:
        return UTILS.HttpResponse(200, { 'Result': 'Inbox is working :)' })

    speed = {}
    started = TIMER.StartWatch()
    validation = validate(envelope, speed)
    execution = execute(validation, envelope, speed)
    speed['Total handling'] = TIMER.StopWatch(started)

    return output(envelope, validation, execution, speed)
    


    

'''
{
    "Header":{
        "Correlation":"bb37d258-015c-497e-8a67-50bf244a9299",
        "Timestamp":"2023-06-24T23:08:24.550719Z",
        "To":"105b4478-eaa5-4b73-b2a5-4da2c3c2dac0.dev.dtfw.org",
        "Subject":"AnyMethod",
        "Code":"dtfw.org/msg",
        "Version":"1",
        "From":"105b4478-eaa5-4b73-b2a5-4da2c3c2dac0.dev.dtfw.org"
    },
    "Body":{
    },
    "Signature": "Lw7sQp6zkOGyJ+OzGn+B1R4rCN/qcYJCtijflQu1Ayqpgxph10yS3KwA4yRhjXgUovskK7LSH+ZqhXm1bcLeMS81l1GKDVaZk3qXpNtrwRmnWrjfD1MekZrO1sRWPNBRH157INAkPWFH/Wb2LLPCAJZYwIv02BF3zKz/Zgm8z7BqOJ3ZrAOC80kTef1zhXNXUMQ/HBrspUTx0NFiMi+dXZMJ69ylxGaAjALMLmcMwFqH2D5cWqX5+eMx0zv2tMh73e8xQqxOr+YLUkO7JjK56KbCUk0HYGUbL5co9eyQMYCGyDtn0G2FqSK9h8BJ1YW3LQmWWTGa/kWDxPjHR3iNyg==", 
    "Hash": "ee6ca2a43ec05d0bd855803407b9350e6c84dd1b981274e51ce0a0a8be16e4a1"
}
'''