import boto3
import json
import os

client = boto3.client('secretsmanager')


def set_secret(name, value):
    print(f'{name=}')
    print(f'{value=}')
    
    try:
        client.create_secret(
            Name=name,
            SecretString=value
        )
    except:
        client.update_secret(
            SecretId=name,
            SecretString=value
        )


def handler(event, context):
    print(f'{event=}')

    set_secret('/dtfw/publicKey', event['publicKey'])
    set_secret('/dtfw/privateKey', event['privateKey'])


'''
{
    "publicKey": "my-public-key",
    "privateKey": "my-private-key"
}
'''