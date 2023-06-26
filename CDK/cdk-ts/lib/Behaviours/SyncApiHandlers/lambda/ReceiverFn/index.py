# 📚 SyncApi.ReceiverFn

from typing import Dict, Optional
import boto3
from urllib import request, parse
import base64
from base64 import b64encode, b64decode
from hashlib import sha256
import os
import json
import copy
import re
import sys

tableName = os.environ['TABLE']
dynamodbClient = boto3.resource('dynamodb')
table = dynamodbClient.Table(tableName)


# 👉 https://www.fernandomc.com/posts/ten-examples-of-getting-data-from-dynamodb-with-python-and-boto3/
def getItem(table, id):
    print (f'{id=}')
    print (f'{tableName=}')

    response = table.get_item(
        Key = { 'ID': id }
    )
    print (f'{response=}')
    
    if 'Item' not in response:
        return None

    item = response['Item']
    print (f'{item=}')
    return item


# 👉 https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/client/invoke.html
lambdaClient = boto3.client('lambda')
def invoke(functionName, params):
    print(f'invoking [{functionName}]({params})...')
    
    response = lambdaClient.invoke(
        FunctionName = functionName,
        Payload=json.dumps(params),
        LogType='Tail')
    ret = json.loads(response['Payload'].read())
    return ret
    
    
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


def getHash(event): 
    envelope = copy.deepcopy(event)
    del envelope['Signature']
    del envelope['Hash']
    canonicalized = canonicalize(envelope)
    digested = digest(canonicalized)
    return { 
        'digested': digested,
        'canonicalized': canonicalized
    }
    

def getPublicKey(event):
    print('getPublicKey...')
        
    if 'Header' not in event:
        return Null
        
    if 'From' not in event['Header']:
        return Null

    resp = invoke(
        os.environ['GET_PUBLIC_KEY_FN'],
        { 'domain': event['Header']['From'] }
    )
    return resp
    
    
def getSubject(event):
    if 'Header' not in event:
        return Null
        
    if 'Subject' not in event['Header']:
        return Null

    subject = event['Header']['Subject']
    return subject
    

def handler(event, context):
    print(f'{event=}')

    received = event
    
    # VALIDATE THE REQUEST
    pub_key = getPublicKey(received)
    rehashed = getHash(received)
    
    # EXECUTE THE ACTION
    subject = getSubject(received)
    target = getItem(table=table, id=subject)
    
    answer = None 
    if (target):
        answer = invoke(
            functionName=target['Target'], 
            params=received)
    
    output = {
        'Executed': {
            'Subject': subject,
            'Target': target,
            'Answer': answer
        },
        'Validated': {
            'PublicKey': pub_key,
            'Rehashed': rehashed['digested'],
            'Canonicalized': rehashed['canonicalized']
        },
        'Received': received
    }

    return output
    

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