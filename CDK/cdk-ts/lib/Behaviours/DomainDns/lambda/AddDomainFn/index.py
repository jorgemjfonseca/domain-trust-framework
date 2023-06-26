# ====================
# Executed on DTFW.ORG
# ====================

from typing import Any
import boto3
 
import base64
import json
from botocore.exceptions import ClientError


r53 = boto3.client('route53')



def get_hosted_zones():
    # https://docs.aws.amazon.com/fr_fr/ses/latest/dg/example_ses_Scenario_ReplicateIdentities_section.html
    zones = []
    zone_paginator = r53.get_paginator('list_hosted_zones')
    zone_iterator = zone_paginator.paginate(PaginationConfig={'PageSize': 20})
    zones = [
        zone for zone_page in zone_iterator for zone in zone_page['HostedZones']]
    print("Found %s hosted zones.", len(zones))
    return zones
    
    
def get_hosted_zone_id(name):
    zones = get_hosted_zones()
    print(f'zones: {zones}')

    # https://docs.aws.amazon.com/fr_fr/ses/latest/dg/example_ses_Scenario_ReplicateIdentities_section.html
    
    for z in zones:
        if z['Name'] == name:
            return z['Id']
    raise Exception('Zone not found: ' + name)
    
    
def record_exists(hosted_zone_id, name):
    result=r53.list_resource_record_sets(HostedZoneId=hosted_zone_id)
    
    for r in result["ResourceRecordSets"]:
        record_name = r["Name"]
        if record_name == name:
            return True
            
    return False


def add_record(hosted_zone_id, type, record_name, value):
    # https://stackoverflow.com/questions/38554754/cant-update-dns-record-on-route-53-using-boto3
            
    changes = [
        {
            "Action": "UPSERT",
            "ResourceRecordSet": {
                "Name": record_name,
                "Type": type,
                "TTL": 60,
                "ResourceRecords": value,
            }
        },
    ]
    
    r53.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            "Comment": "Automatic DNS update",
            "Changes": changes
        })
        

def process_request(event):
    print(f'{event=}')
    
    if 'domain' not in event:
        print(f'Domain not sent')
        return 
    
    if 'servers' not in event:
        print(f'Servers not sent')
        return
    
    parent = 'dev.dtfw.org.'  
    
    child = event['domain']
    if not child.endswith('.'+parent):
        print(f'Not a dev domain')
        return
    
    servers = event['servers'].split(',')
    if len(servers) != 4:
        print(f'Not 4 servers')
        return
    
    hosted_zone_id = get_hosted_zone_id(parent)
    if False and record_exists(hosted_zone_id, child):
        print(f'Record exists')
        return
    
    value = [{'Value': ns} for ns in servers]
    print(f'Adding {child}={value}')
    add_record(hosted_zone_id, 'NS', child, value)


def lambda_handler(event, context):
    
    if 'queryStringParameters' in event:
        event = event['queryStringParameters']
        
    process_request(event)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello world!')
    }


'''
{
    "servers": "ns-759.awsdns-30.net.,ns-1176.awsdns-19.org.,ns-1617.awsdns-10.co.uk.,ns-237.awsdns-29.com.", 
    "domain": "cf41fa0a-5bbf-4123-8473-6c44e5721323.dev.dtfw.org."
}
'''
