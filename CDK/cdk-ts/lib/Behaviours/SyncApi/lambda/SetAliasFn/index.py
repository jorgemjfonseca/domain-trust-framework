# https://medium.com/cyberark-engineering/advanced-custom-resources-with-aws-cdk-1e024d4fb2fa

from typing import Any
import boto3

import urllib.request

import base64
import argparse
import json
import logging
from pprint import pprint
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

api = boto3.client('apigateway')
r53 = boto3.client('route53')
cfn = boto3.client('cloudformation')


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

    