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
from copy import deepcopy


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
        

    
# 👉️ https://bobbyhadz.com/blog/python-json-dumps-no-spaces
def canonicalize(object: any) -> str:
    canonicalized = json.dumps(object, separators=(',', ':'))
    print(f'{canonicalized=}')
    return canonicalized    


# REQUEST { hostname }
# RESPONSE: str
def invokeDkimReader(event):
    domain = event['Header']['From']
    hostname = 'dtfw._domainkey.' + domain
    return invoke(
        os.environ['DKIM_READER_FN'],
        { 
            'hostname': hostname 
        })
    


def getFrom(event):
    return event['Header']['From']


def getTo(event):
    return event['Header']['To']
    

def getSubject(event):
    return event['Header']['Subject']
    

def validateTo(received: any):
    if getTo(received).lower() != os.environ['DOMAIN_NAME']:
        a = getTo(received).lower()
        b = os.environ['DOMAIN_NAME']
        raise Exception(f'Wrong domain. Expected [{b}], but received [{a}].')


# REQUEST { text, publicKey, signature }
# RESPONSE { hash, isVerified }
def invokeValidator(text, publicKey, signature):
    invoke(os.environ['VALIDATOR_FN'], {
        'text': text,
        'publicKey': publicKey,
        'signature': signature
    })


def validateSignature(received: any):
    
    copy = deepcopy(received)
    del copy['Signature']
    del copy['Hash']
    text = canonicalize(copy)

    publicKey = invokeDkimReader(received)
    signature = received['Signature']
    verification = invokeValidator(text, publicKey, signature)

    if verification['hash'] != received['Hash']:
        a = verification['hash']
        b = received['Hash']
        raise Exception(f'Wrong hash: expected [{a}] but received [{b}].')

    if not verification['isVerified']:
        raise Exception(f'Signature not valid.')



def handler(event, context):
    print(f'{event=}')

    received = event
    validateTo(received)
    validateSignature(received) 
    
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