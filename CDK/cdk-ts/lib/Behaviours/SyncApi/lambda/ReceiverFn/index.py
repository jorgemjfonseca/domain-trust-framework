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

tableName = os.environ('TABLE_Map')
dynamodbClient = boto3.client('dynamodb')


# 👉 https://www.fernandomc.com/posts/ten-examples-of-getting-data-from-dynamodb-with-python-and-boto3/
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


# 👉 https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/client/invoke.html
lambdaClient = boto3.client('lambda')
def invoke(functionName, params):
    return lambdaClient.invoke(
        FunctionName = functionName,
        Payload=json.dumps(params),
        LogType='Tail')


# 👉 https://blog.knoldus.com/how-to-create-an-eventbridge-application-in-python/
# 👉 https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html
# 👉 https://boto3.amazonaws.com/v1/documentation/api/1.10.46/reference/services/events.html
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


# 👉 https://github.com/kmille/dkim-verify
def get_public_key(domain: str, selector: str):
    dns_response = dns.resolver.query("{}._domainkey.{}.".format(selector, domain), "TXT").response.answer[0].to_text()
    p = re.search(r'p=([\w\d/+]*)', dns_response).group(1)
    pub_key = RSA.importKey(b64decode(p))
    return pub_key
    




def handler(event, context):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": "hello :)"
    }
    
    action = envelope['action']
    
    target = getItem(tableName=tableName, id=action)

    return invoke(
        functionName=target['name'], 
        params=envelope)

'''
{
  "Header": {
    "Correlation": "53675692-1064-4ce2-a304-1a8b58541b2f",
    "Timestamp": "2023-06-23T19:23:32.489913Z",
    "To": "7b61af20-7518-4d5a-b7c0-eee17e54bf7a.dev.dtfw.org",
    "Subject": "AnyMethod",
    "Code": "dtfw.org/msg",
    "Version": "1",
    "From": "7b61af20-7518-4d5a-b7c0-eee17e54bf7a.dev.dtfw.org"
  },
  "Body": {},
  "Signature": "W7HvsldzbP65Evd0HY87HITB4BLwU4F89XYsy4V5f5GP1cM0dXoqu5Liepfx4/AgAoLbi5J2go7mkbLHYbqzeq4jkjgG2MrMNmfc/DHRs2DOAtn4vTgv1U8caalfx+W394U6DdzkHnMyBSpvWzX5EsDu+LNWnpFLZ905YTQRLlkHvaI3rqgtvrjr9nPugn/Y+NuujIcvehVZPecLNX75LhaKMaBUVak3L74AL/YF+N9r0aay+Jp78w8ZlVOgn3QYV6x6/8fXWc16foX4x8uYMfRqDyZoAjaPn30I3vTOdnuVSOVQ7LB4w/b9gBanvqhjix5WpKrp+exuJfHu3s5B3g==", 
  "Hash": "416ffa44a7adc6dfce6bd7811da5862e6602cb135819aa06a86cd73ef4c63576"
}
'''