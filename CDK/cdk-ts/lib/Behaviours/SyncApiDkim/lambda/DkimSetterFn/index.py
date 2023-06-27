# SyncApiDkim-DkimSetterFn

import boto3
import json
import os


r53 = boto3.client('route53')
    

# 👉 https://stackoverflow.com/questions/38554754/cant-update-dns-record-on-route-53-using-boto3
def update_record(hosted_zone_id, record_name, value):
    
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
    print(f'{changes=}')
    
    r53.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            "Comment": "Automatic DNS update",
            "Changes": changes
        })
        

   
# 👉 https://repost.aws/knowledge-center/route53-resolve-dkim-text-record-error
def add_dkim_record(hosted_zone_id, public_key, record_name):
    
    dkim = public_key[:200] + '""' + public_key[200:]
    update_record(
        hosted_zone_id = hosted_zone_id, 
        record_name = record_name, 
        value = f'"v=DKIM1;k=rsa;p={dkim};"')    
    


def handler(event, context):
    print(f'{event=}')
    
    public_key = event['public_key']
    public_key = public_key.replace('-----BEGIN PUBLIC KEY-----', '')
    public_key = public_key.replace('-----END PUBLIC KEY-----', '')
    public_key = public_key.replace('\n', '')

    add_dkim_record(
        hosted_zone_id = os.environ['hostedZoneId'], 
        public_key = public_key, 
        record_name = os.environ['dkimRecordName'])
