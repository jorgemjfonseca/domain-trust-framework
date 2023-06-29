# ====================
# Executed on DTFW.ORG
# ==================== 

from typing import Any
import boto3
 
import base64
import json
from botocore.exceptions import ClientError


r53 = boto3.client('route53')
r53domains = boto3.client('route53domains')



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
    
    
def record_exists(hosted_zone_id, name, type):
    result=r53.list_resource_record_sets(HostedZoneId=hosted_zone_id)
    
    for r in result["ResourceRecordSets"]:
        record_name = r["Name"]
        record_type = r["Type"]
        if record_name == name and record_type == type:
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
    print(f'{changes=}')
    
    r53.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            "Comment": "Automatic DNS update",
            "Changes": changes
        })
        
        
def parse(event):
    print(f'PARSE ==== {event=}')
    
    if 'domain' not in event:
        print(f'Domain not sent')
        return { 'e': 'Domain not sent' }
        
    parent = 'dev.dtfw.org.'  
    
    child = event['domain']
    if not child.endswith('.'+parent):
        print(f'Not a dev domain')
        return { 'e': 'Not a dev domain' }
        
    hosted_zone_id = get_hosted_zone_id(parent)
    
    return { 
        'zone': hosted_zone_id,
        'child': child
    }        
        

def add_ns_records(event, parsed):
    print(f'ADD NS ==== {event=}')
    
    if 'servers' not in event:
        print(f'Servers not sent')
        return { 'e': 'Servers not sent' }
    
    servers = event['servers'].split(',')
    if len(servers) != 4:
        print(f'Not 4 servers')
        return { 'e': 'Not 4 servers' }
    
    hosted_zone_id = parsed['zone']
    child = parsed['child']
    
    # Ensure that domains, once created, cannot be pointed to other Name Servers.
    if record_exists(hosted_zone_id, child, 'NS'):
        print(f'NS record exists, ignoring for security.')
        return { 'e': 'NS record exists, ignoring for security.' }
    
    value = [{'Value': ns} for ns in servers]
    print(f'Adding NS {child}={value}')
    add_record(hosted_zone_id, 'NS', child, value)
    
    return None
    
    
# 👉 https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/associate_delegation_signer_to_domain.html
# 👉 https://docs.aws.amazon.com/Route53/latest/APIReference/API_domains_DnssecSigningAttributes.
# 👉 https://github.com/hashicorp/terraform-provider-aws/issues/28749
# 👉 https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-configuring-dnssec-enable-signing.html
# 👉 https://dnssec-analyzer.verisignlabs.com/dev.dtfw.org
# 👉 https://dnssec-analyzer.verisignlabs.com/dtfw.org
# 👉 https://www.performancemagic.com/route-53-dnssec/
# 👉 https://dnsviz.net/d/dev.dtfw.org/dnssec/
def add_ds_record(event, parsed):
    print(f'ADD DS ==== {event=}')
    
    if 'dnssec' not in event:
        print(f'DnsSec public key not sent')
        return { 'e': 'DnsSec public key not sent' }
    
    dnssec = event['dnssec']
    
    hosted_zone_id = parsed['zone']
    child = parsed['child']
    
    # Ensure that domains, once created, cannot be pointed to other Name Servers.
    if record_exists(hosted_zone_id, child, 'DS'):
        print(f'DS record exists, ignoring for security.')
        return { 'e': 'DS record exists, ignoring for security.' }
    
    print(f'Adding DS for {child=}')
    add_record(
        hosted_zone_id, 
        'DS', child, [{
            'Value': dnssec
        }])
    
    '''
    add_record(
        get_hosted_zone_id('dtfw.org.'), 
        'DS', 'dev.dtfw.org.', [{
            'Value': '11328 13 2 4D88A5CC7A1F21A86AD9A06A058D4EEC16224C4978F07193E2F14519962C4EBA'
        }])
    '''
    
    return None
    

def lambda_handler(event, context):
    
    if 'queryStringParameters' in event:
        event = event['queryStringParameters']
        
    parsed = parse(event)
    if ('e' in parsed):
        return {
            'statusCode': 400,
            'body': parsed['e']
        }    
        
    added_ns = add_ns_records(event, parsed)
    if (added_ns != None and 'e' in added_ns):
        return {
            'statusCode': 400,
            'body': added_ns['e']
        }    
        
    added_ds = add_ds_record(event, parsed)
    if (added_ds != None and 'e' in added_ds):
        return {
            'statusCode': 400,
            'body': added_ds['e']
        }    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello world!')
    }


'''
{
    "servers": "ns-759.awsdns-30.net.,ns-1176.awsdns-19.org.,ns-1617.awsdns-10.co.uk.,ns-237.awsdns-29.com.", 
    "domain": "cf41fa0a-5bbf-4123-8473-6c44e5721323.dev.dtfw.org.",
    "dnssec": "43563 13 2 13534ECFA3E1A51EF1BEDD243358CC2434D4BAC234D9A938C6F9E72D2AE21AB8"
}
'''
