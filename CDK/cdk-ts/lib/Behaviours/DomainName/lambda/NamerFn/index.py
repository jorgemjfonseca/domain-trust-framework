# https://medium.com/cyberark-engineering/advanced-custom-resources-with-aws-cdk-1e024d4fb2fa

from DTFW import DTFW

def on_create(event):
    DTFW().Domain().HandleNamerCreate()    
    return {'PhysicalResourceId': 'custom'}


def on_update(event):
    return {'PhysicalResourceId': 'custom'}


def on_delete(event):
    DTFW().Domain().HandleNamerDelete()    
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