#!/usr/bin/env python3

import boto3
import os
import json


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
    

def handler(event, context):
    print(f'{event=}')

    return 'TODO'
    

    


'''

'''