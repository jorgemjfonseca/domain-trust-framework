# 📚 SyncApiHandlers-ReceiverFn
# TODO: on [handler], catch internal validation exceptions, and return a 400

import boto3
from urllib.request import urlopen
import os
import json
from copy import deepcopy
import datetime


table = None
def db():
    global table
    if not table:
        tableName = os.environ['TABLE']
        print (f'{tableName=}')
        
        dynamodbClient = boto3.resource('dynamodb')
        table = dynamodbClient.Table(tableName)
    return table


# 👉 https://www.fernandomc.com/posts/ten-examples-of-getting-data-from-dynamodb-with-python-and-boto3/
def getItem(table, id):
    print (f'{id=}')

    response = table.get_item(
        Key = { 'ID': id }
    )
    print (f'getItem: {response=}')
    
    if 'Item' not in response:
        return None

    item = response['Item']
    print (f'{item=}')
    return item


# 👉 https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/client/invoke.html
lambdaClient = boto3.client('lambda')
def invoke(functionName, params):
    print(f'{elapsed()} invoke.invoking [{functionName}]({params})...')
    
    response = lambdaClient.invoke(
        FunctionName = functionName,
        Payload=json.dumps(params),
        LogType='Tail')
    ret = json.loads(response['Payload'].read())
    
    print(f'invoke.returning {ret}')
    return ret
        

    
# 👉️ https://bobbyhadz.com/blog/python-json-dumps-no-spaces
def canonicalize(received: any) -> str:
    print(f'{elapsed()} Canonicalizing...')

    copy = deepcopy(received)
    del copy['Signature']
    del copy['Hash']

    canonicalized = json.dumps(copy, separators=(',', ':'))
    print(f'{canonicalized=}')
    return canonicalized    


# REQUEST { hostname }
# RESPONSE: str
# 👉️ https://developers.google.com/speed/public-dns/docs/doh
# 👉️ https://developers.google.com/speed/public-dns/docs/doh/json
# 👉️ https://dns.google/resolve?name=dtfw._domainkey.38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org&type=TXT&do=1
def invokeDkimReader(envelope, checks):
    print(f'{elapsed()} Invoke dns.google...')
    
    header = getHeader(envelope)
    domain = getHeaderFrom(header)
    hostname = f'dtfw._domainkey.{domain}'
    checks.append(f'Valid domain?: {hostname}')
    
    url = f'https://dns.google/resolve?name={hostname}&type=TXT&do=1'
    with urlopen(url) as response:
        body = response.read()

    print(f'{elapsed()} Validate dns.google...')
    resp = json.loads(body)
    isDnsSec = (resp['AD'] == True)
    checks.append(f'IsDnsSec?: {isDnsSec}')
    if not isDnsSec:
        raise Exception(f"Sender is not DNSSEC protected.")
    
    dkim = None
    exists = 'Answer' in resp
    checks.append(f'Exists?: {exists}')
    if exists:
        for answer in resp['Answer']:
            if answer['type'] == 16:
                dkim = answer['data']

    isDkimSetUp = (dkim != None)
    checks.append(f'DKIM set?: {isDkimSetUp}')
    if not isDkimSetUp:
        raise Exception(f"Sender DKIM not found for dtfw.")
    
    public_key = None
    for part in dkim.split(';'):
        elems = part.split('=')
        if elems[0] == 'p' and len(elems) == 2:
            public_key = elems[1];
    
    hasPublicKey = (public_key != None)
    checks.append(f'Public Key set?: {hasPublicKey}')
    if not hasPublicKey:
        raise Exception(f"Public key not found on sender DKIM.")
    
    return public_key
    

# REQUEST { hostname }
# RESPONSE: str
def invokeDkimReader_deprecated(event):
    print(f'invokeDkimReader: {event=}')
    
    domain = event['Header']['From']
    hostname = f'dtfw._domainkey.{domain}'
    return invoke(
        os.environ['DKIM_READER_FN'],
        { 
            'hostname': hostname 
        })    


def getHeader(event):
    #print(f'getHeader: {event=}')
    if 'Header' not in event:
        raise Exception(f'Header missing!')
    return event['Header']


def getHeaderFrom(header):
    print(f'getHeaderFrom: {header=}')
    if 'From' not in header or header['From'] == '':
        raise Exception(f'Header.From missing!')
    return header['From']


def getHeaderTo(header):
    #print(f'getHeaderTo: {header=}')
    if 'To' not in header or header['To'].strip() == '':
        raise Exception(f'Header.To missing!')
    return header['To']
    

def getHeaderSubject(header):
    #print(f'getHeaderSubject: {header=}')
    if 'Subject' not in header or header['Subject'].strip() == '':
        raise Exception(f'Header.Subject missing!')
    return header['Subject']


def getSignature(envelope):
    #print(f'getSignature: {envelope=}')
    if 'Signature' not in envelope or envelope['Signature'].strip() == '':
        raise Exception(f'Signature missing!')
    return envelope['Signature']
    

def getHash(envelope):
    #print(f'getHash: {envelope=}')
    if 'Hash' not in envelope:
        raise Exception(f'Hash missing!')
    return envelope['Hash']


def getBody(envelope):
    #print(f'getBody: {envelope=}')
    
    if 'Body' not in envelope or envelope['Body'] == '':
        raise Exception(f'Body missing!')

    return envelope['Body']


def validateTo(envelope: any, checks):
    #print(f'validateTo: {envelope=}')
    
    header = getHeader(envelope)
    to = getHeaderTo(header).lower()
    me = os.environ['DOMAIN_NAME']

    if to != me:
        raise Exception(f'Wrong domain. Expected [{me}], but received [{to}]!')
    checks.append(f'For me?: {True}')


# REQUEST { text, publicKey, signature }
# RESPONSE { hash, isVerified }
def invokeValidator(text, publicKey, signature):
    print(f'{elapsed()} Invoking validator...')

    validator = invoke(os.environ['VALIDATOR_FN'], {
        'text': text,
        'publicKey': publicKey,
        'signature': signature
    })
    print(f'{validator=}')
    return validator;


def validateHash(envelope, validator, checks):
    expected = validator['hash']
    received = getHash(envelope)
    
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
    print(f'{elapsed()} Validating signature...')
    
    started = startWatch()
    signature = getSignature(envelope)
    text = canonicalize(envelope)
    publicKey = invokeDkimReader(envelope, checks)
    speed['Get DKIM over DNSSEC'] = stopWatch(started)

    started = startWatch()
    validator = invokeValidator(text, publicKey, signature)
    validateHash(envelope, validator, checks)
    validateSignature(validator, checks)
    speed['Verify signature'] = stopWatch(started)


def validateHeader(envelope):
    print(f'{elapsed()} Validating header...')

    header = getHeader(envelope)
    getHeaderTo(header)
    getHeaderSubject(header)


def validate(envelope, speed):
    print(f'{elapsed()} Validating...')
    
    error = None
    checks = []
    
    try:
        validateHeader(envelope)
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
    print(f'{elapsed()} Executing...')
    started = startWatch()

    if validation['Error']:
        ret = { 
            'Result': 'Ignored, invalid envelope!'
        }
        print(f'{ret=}')
        return ret

    header = getHeader(envelope)
    subject = getHeaderSubject(header)
    target = getItem(table=db(), id=subject)
    
    answer = None 
    if (target):
        answer = invoke(
            functionName=target['Target'], 
            params=envelope)

    ret = {
        'Result': 'Executed',
        'Target': target,
        'Answer': answer
    }    
    print(f'{ret=}')

    speed['Execute method'] = stopWatch(started)
    return ret


def httpResponse(code, body):
    return {
        'statusCode': code,
        'body': json.dumps(body)
    }


def output(envelope, validation, execution, speed):
    print(f'{elapsed()} Building the output...')

    output = {
        'Speed': speed,
        'Execution': execution,
        'Validation': validation,
        'Received': envelope
    }

    print ('Returning...')
    if validation['Error']:
        return httpResponse(400, output)
    return httpResponse(200, output)


def startWatch():
    return datetime.datetime.now()

def stopWatch(start):
    current = datetime.datetime.now()
    elapsed = (current - start)
    output = round(elapsed.total_seconds() * 1000)
    return f'{output} ms'
    

timerStart = datetime.datetime.now()
def elapsed():
    global timerStart
    current = datetime.datetime.now()
    elapsed = (current - timerStart)
    timerStart = current
    output = round(elapsed.total_seconds() * 1000)
    return f'''--> Elapsed: {output} ms
.
'''

def printElapsed():
    print(f"--- {elapsed()} milliseconds elapsed")


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
        return httpResponse(200, { 'Result': 'Inbox is working :)' })

    speed = {}
    started = startWatch()
    validation = validate(envelope, speed)
    execution = execute(validation, envelope, speed)
    speed['Total handling'] = stopWatch(started)

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