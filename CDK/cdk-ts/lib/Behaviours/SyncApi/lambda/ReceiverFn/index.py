#!/usr/bin/env python3

from typing import Dict, Optional
import boto3
from urllib import request, parse
import base64
from base64 import b64encode, b64decode
import os
import json

import re
import sys
import dns.resolver


# https://www.fernandomc.com/posts/ten-examples-of-getting-data-from-dynamodb-with-python-and-boto3/
dynamodbClient = boto3.client('dynamodb')
def getItem(tableName, id):
    print (f'{id=}')
    print (f'{tableName=}')

    response = dynamodbClient.get_item(
        TableName = tableName,
        Key = { 'ID': {'S': id} }
    )

    item = response['Item']
    print (f'{item=}')

    obj = json.loads(item['Json'])
    return obj


# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/client/invoke.html
lambdaClient = boto3.client('lambda')
def invoke(functionName, params):
    return lambdaClient.invoke(
        FunctionName = functionName,
        Payload=json.dumps(params),
        LogType='Tail')


# https://blog.knoldus.com/how-to-create-an-eventbridge-application-in-python/
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html
# https://boto3.amazonaws.com/v1/documentation/api/1.10.46/reference/services/events.html
eventsClient = boto3.client('events')
def publish(eventBusName, source, detailType, detail):
    return eventsClient.put_events(
        Entries=[
            {
                'Source':source,
                'DetailType':detailType,
                'Detail':detail,
                'EventBusName':eventBusName
            }
        ]
)


# https://github.com/kmille/dkim-verify
def get_public_key(domain: str, selector: str) -> RSA.RsaKey:
    dns_response = dns.resolver.query("{}._domainkey.{}.".format(selector, domain), "TXT").response.answer[0].to_text()
    p = re.search(r'p=([\w\d/+]*)', dns_response).group(1)
    pub_key = RSA.importKey(b64decode(p))
    return pub_key
    




def handler(event):
    envelope = event['envelope']
    
    action = envelope['action']
    tableName = os.environ('TABLE_Map')
    target = getItem(tableName=tableName, id=action)

    return invoke(
        functionName=target['name'], 
        params=envelope)
