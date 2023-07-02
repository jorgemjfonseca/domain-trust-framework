# https://medium.com/cyberark-engineering/advanced-custom-resources-with-aws-cdk-1e024d4fb2fa


def on_create(event):
    print(f'on_create: {event}')

    import os
    hosted_zone_id = os.environ['hostedZoneId']  

    from DTFW import DTFW
    DTFW.RegisterDomain(hosted_zone_id)
    
    return {'PhysicalResourceId': 'custom'}


def on_update(event):
    print(f'on_update: {event}')
    return on_create(event)


def on_delete(event):
    print(f'on_delete: {event}')
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