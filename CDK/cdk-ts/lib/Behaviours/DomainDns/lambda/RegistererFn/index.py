# https://medium.com/cyberark-engineering/advanced-custom-resources-with-aws-cdk-1e024d4fb2fa

import boto3
import urllib.request

r53 = boto3.client('route53')


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