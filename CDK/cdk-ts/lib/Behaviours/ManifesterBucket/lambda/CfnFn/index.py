# ManifesterBucket-CfnFn

# 👉 https://medium.com/cyberark-engineering/advanced-custom-resources-with-aws-cdk-1e024d4fb2fa

import boto3
import json
import os

client = boto3.client('s3')  

def process():
    
    domainName = os.environ['DOMAIN_NAME']

    body = f"""
Identity:
  Domain: {domainName}
  Name: Random Domain
  SmallIcon: https://picsum.photos/20/20
  BigIcon: https://picsum.photos/100/100
  Translations: 
    - Language: en-us
      Translation: Random Domain
    - Language: pt-br
      Translation: Domínio Aleatório
"""
    
    client.put_object(
        Body = body, 
        Bucket = os.environ['BUCKET_NAME'], 
        Key = os.environ['FILE_NAME'])



def on_create(event):
    if 'ResourceProperties' in event:
        props = event["ResourceProperties"]
        print(f'create new resource with {props=}')

    process()
    
    return {'PhysicalResourceId': 'custom'}


def on_update(event):
    physical_id = event["PhysicalResourceId"]
    props = event["ResourceProperties"]
    old_props = event["OldResourceProperties"]
    print(f'update resource {physical_id} with {props=}, {old_props=}')

    return on_create(event)


def on_delete(event):
    return {'PhysicalResourceId': 'custom'}

    

def on_event(event, context):
    print(event)
     
    if 'RequestType' not in event:
        return on_create(event)
    
    request_type = event['RequestType'].lower()
    if request_type == 'create':
        return on_create(event)
    if request_type == 'update':
        return on_update(event)
    if request_type == 'delete':
        return on_delete(event)
    raise Exception(f'Invalid request type: {request_type}')



def handler(event, context):
    on_event(event, context)