# https://medium.com/cyberark-engineering/advanced-custom-resources-with-aws-cdk-1e024d4fb2fa

import boto3

ssm = boto3.client('ssm')


    
# 👉 https://www.sufle.io/blog/how-to-use-ssm-parameter-store-with-boto3
def name_domain(props):
    paramName = props['paramName']
    domainName = props['domainName']
    
    try:
        param = ssm.get_parameter(Name=paramName)['Parameter']['Value']
    except:
        param = None

    if (param):
        print(f'Parameter already set, ignoring: ' + param)
        return
    else:
        print(f'Setting new parameter: ' + domainName)
        ssm.put_parameter(Name=paramName, Value=domainName, Type="String")
    

def on_create(event):
    props = event["ResourceProperties"]
    print(f'create new resource with {props=}')

    name_domain(props)
    
    return {'PhysicalResourceId': 'custom'}


def on_update(event):
    return {'PhysicalResourceId': 'custom'}


def on_delete(event):
    ssm.delete_parameter(Name=event["ResourceProperties"]['paramName'])
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
    
    

'''
{
    "ResourceProperties": {
        "paramName": "/dtfw/DomainName",
        "domainName": "my-domain-name"
    }
}
'''