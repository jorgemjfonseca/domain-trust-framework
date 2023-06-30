# 📚 Publisher.Register

# 👉 https://quip.com/sBavA8QtRpXu/-Publisher#temp:C:IEKf5f88769121840418de6755e4

import boto3
import json
import os

db = boto3.client('dynamodb')
table = db.Tables(os.environ[''])


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

    
    

def update_record(props: any):
    print(f'{props=}')
    
    changes = [
        {
            "Action": "UPSERT",
            "ResourceRecordSet": {
                "Name": props['customDomain'],
                "Type": 'A',
                'AliasTarget': {
                    'HostedZoneId': props['apiHostedZoneId'],
                    'DNSName': props['apiAlias'],
                    'EvaluateTargetHealth': True
                }
            }
        },
    ]
    print(f'{changes=}')
    
    r53.change_resource_record_sets(
        HostedZoneId = props['hostedZoneId'],
        ChangeBatch = {
            "Comment": 'API Gateway custom domain',
            "Changes": changes
        })
        
       
       

def on_create(event):
    if 'ResourceProperties' in event:
        props = event["ResourceProperties"]
        print(f'create new resource with {props=}')

    update_record(props)
        
    return {'PhysicalResourceId': 'custom'}


def on_update(event):
    physical_id = event["PhysicalResourceId"]
    props = event["ResourceProperties"]
    old_props = event["OldResourceProperties"]
    print(f'update resource {physical_id} with {props=}, {old_props=}')

    return on_create(event)


def on_delete(event):
    physical_id = event["PhysicalResourceId"]
    props = event["ResourceProperties"]
    return {'PhysicalResourceId': 'custom'}

    