# 📚 Subscriber.SubscriberFn

# 👉 https://quip.com/sBavA8QtRpXu/-Publisher#temp:C:IEKf5f88769121840418de6755e4

import boto3
import json
import os
import dtfw 

dynamo = boto3.resource('dynamodb')
table = dynamo.Table(os.environ['SUBSCRIBERS'])


def handler(event, context):
    print(f'{event}')
    return dtfw.test()