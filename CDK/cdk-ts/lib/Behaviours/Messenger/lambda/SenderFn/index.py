# 📚 Messenger-SenderFn

import boto3
from urllib import request, parse
import os
import json
import uuid
import datetime



# 👉 https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/client/invoke.html
lambdaClient = boto3.client('lambda')
def invoke(functionName, params):
    print(f'invoking [{functionName}]({params})...')
    
    response = lambdaClient.invoke(
        FunctionName = functionName,
        Payload=json.dumps(params),
        LogType='Tail')
    
    returned = json.loads(response['Payload'].read())
    print(f'{returned=}')
    return returned


# 👉️ https://stackoverflow.com/questions/53676600/string-formatting-of-utcnow
def timestamp():
    timestamp = datetime.datetime.utcnow().isoformat() + 'Z'
    print(f'{timestamp=}')
    return timestamp


# 👉️ https://stackoverflow.com/questions/37049289/how-do-i-convert-a-python-uuid-into-a-string
def correlation():
    correlation = str(uuid.uuid4());
    print(f'{correlation=}')
    return correlation



def wrap_envelope(message: any):
    defaults = {
        'Header': {
            'Correlation': correlation(),
            'Timestamp': timestamp()
        },
        'Body': {}
    }
    print(f'{defaults=}')

    # 👉️ https://stackoverflow.com/questions/14839528/merge-two-objects-in-python
    envelope = defaults
    envelope['Header'].update(message['Header']) 
    if 'Body' in message:
        envelope['Body'].update(message['Body']) 

    return envelope


def send_envelope(envelope):
    return invoke(
        functionName= os.environ['SENDER'],
        params= envelope)

   

# 👉️ https://quip.com/NiUhAQKbj7zi
def handler(event, context):
    print(f'{event=}')

    message = event
    envelope = wrap_envelope(message)
    sent = send_envelope(envelope)
    return sent
    

'''
{ 
    "Header": {
        "To": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org",
        "Subject": "AnyMethod"
    }
}
'''    