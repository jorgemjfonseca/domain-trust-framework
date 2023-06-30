# 📚 ManifesterAlerter.AlerterFn

import boto3
import os
import json


# 👉️ https://docs.aws.amazon.com/appconfig/latest/userguide/working-with-appconfig-extensions-about-predefined-notification-sqs.html
def handler(event, context):
    print(f'{event=}')
    
    if event['Type'] == 'OnDeploymentComplete':
        print('send message to Listener')


'''
{
   "Type":"OnDeploymentComplete"
}
'''