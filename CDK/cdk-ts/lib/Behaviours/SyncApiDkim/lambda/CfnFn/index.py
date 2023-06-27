# SyncApiDkim-CfnFn

# 👉 https://medium.com/cyberark-engineering/advanced-custom-resources-with-aws-cdk-1e024d4fb2fa

import boto3
import json
import os
    

def process():
    invoke(os.environ['KeyPairRotatorFn'])



# 👉 https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/client/invoke.html
lambdaClient = boto3.client('lambda')
def invoke(functionName, params={}):
    print(f'invoking [{functionName}]({params})...')
    
    response = lambdaClient.invoke(
        FunctionName = functionName,
        Payload=json.dumps(params),
        LogType='Tail')
    ret = json.loads(response['Payload'].read())
    return ret



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
