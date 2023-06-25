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

r53 = boto3.client('route53')
cfn = boto3.client('cloudformation')
kms = boto3.client('kms')


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


def find_ns_record(hosted_zone_id):
    result=r53.list_resource_record_sets(HostedZoneId=hosted_zone_id)
    
    for r in result["ResourceRecordSets"]:
        if r["Type"] == 'NS':
            return r
            
    raise Exception('No record NS found')
    

def update_record(hosted_zone_id, record_name, value):
    # https://stackoverflow.com/questions/38554754/cant-update-dns-record-on-route-53-using-boto3
            
    changes = [
        {
            "Action": "UPSERT",
            "ResourceRecordSet": {
                "Name": record_name,
                "Type": "TXT",
                "TTL": 60,
                "ResourceRecords": [
                    {
                        "Value": value
                    },
                ],
            }
        },
    ]
    
    r53.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            "Comment": "Automatic DNS update",
            "Changes": changes
        })
        
        
def get_public_key(keyId):
    response = kms.get_public_key(
        KeyId=keyId,
        GrantTokens=[
            'string',
        ]
    )
    print(f'response: {response=}')
    base64_bytes = response['PublicKey']
    base64_message = base64.b64encode(base64_bytes)
    print(f'base64_message1: {base64_message=}')
    
    base64_message = base64_message.decode()
    print(f'base64_message2: {base64_message=}')
    
    return base64_message
    
    
def add_dkim_record(hosted_zone_id, keyId, record_name):
    
    public_key = get_public_key(keyId)

    # https://repost.aws/knowledge-center/route53-resolve-dkim-text-record-error
    dkim = public_key[:200] + '""' + public_key[200:]
    
    update_record(hosted_zone_id, record_name, f'"v=DKIM1;k=rsa;p={dkim};"')
    
    
# 👉 host -t NS 105b4478-eaa5-4b73-b2a5-4da2c3c2dac0.dev.dtfw.org
def register_domain(hosted_zone_id):
    ns = find_ns_record(hosted_zone_id)
    print (f'{ns=}')
    
    domain = ns['Name']
    
    servers = []
    for s in ns['ResourceRecords']:
        servers.append(s['Value'])
    serverList = ','.join(servers)
    
    url = f'https://z6jsx3ldteaiewnhm4dwuhljzi0vrxgn.lambda-url.us-east-1.on.aws/?domain={domain}&servers={serverList}'
    print (f'{url=}')
    
    # https://stackoverflow.com/questions/37819525/lambda-function-to-make-simple-http-request/71127429#71127429
    urllib.request.urlopen(urllib.request.Request(
        url=url,
        headers={'Accept': 'application/json'},
        method='GET'),
        timeout=20)
    

def on_create(event):
    if 'ResourceProperties' in event:
        props = event["ResourceProperties"]
        print(f'create new resource with {props=}')

    hosted_zone_id = props['hostedZoneId']
    keyId = props['signatureKeyArn']
    record_name = props['dkimRecordName']

    add_dkim_record(hosted_zone_id, keyId, record_name)
    
    register_domain(hosted_zone_id)
    
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

    