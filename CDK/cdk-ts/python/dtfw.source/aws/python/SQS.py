# 📚 SQS

import boto3
import os
import json

from STRUCT import STRUCT
# 👉 https://stackoverflow.com/questions/24853923/type-hinting-a-collection-of-a-specified-type
from typing import List, Set, Tuple, Dict

from UTILS import UTILS



def test():
    return 'this is a SQS test.'


sqs = boto3.client("sqs")
class SQS(UTILS):
    

    def __init__(self, alias=None):
        if alias != None:
            name = os.environ[alias]
            self.url = sqs.get_queue_url(QueueName= name)
        

    def Send(self, msg):
        ''' 👉 Sends a message to the SQS Queue. '''
        body= msg
        if isinstance(msg, STRUCT):
            body= msg.Obj()
            
        resp = sqs.send_message(
            QueueName= self.url,
            MessageBody= json.dumps(body)
        )
        
        code = resp['ResponseMetadata']['HTTPStatusCode']
        if code != 200:
            raise Exception('Error sending to the queue.')
        return resp
    

    def IsSqsEvent(self, obj:any):
        ''' 👉 Indicates if the object is an SQS response.'''
        if obj == None:
            return False
        if 'Messages' in obj and 'ResponseMetadata' in obj:
            return True
        return False
    
    
    def ParseMessages(self, obj: any) -> List[STRUCT]:
        ''' 👉 Returns the messages inside an SQS response.
        👉 https://stackoverflow.com/questions/58191688/how-to-parse-sqs-json-message-with-python
        {
            'Messages': [
                {
                    'MessageId': '37b13967-a92e-4b8b-8aef-32341a8e1e32',
                    'ReceiptHandle': 'xyz',
                    'MD5OfBody': '081f4bdad6fd3d53c88f165a884a39da',
                    'Body': '{"inputIDList":["1234","5678"],"eventID":"9337","scheduleEvent":false,"addToList":true,"listID":"7654","clientID":"123-ABC-456"}'
                }
            ],
            'ResponseMetadata': {
                'RequestId': '79dafe96-04d9-5122-8b2a-a89b79a76a46',
                'HTTPStatusCode': 200,
                'HTTPHeaders': {
                    'x-amzn-requestid': '79dafe96-04d9-5122-8b2a-a89b79a76a46',
                    'date': 'Tue, 01 Oct 2019 16:13:50 GMT',
                    'content-type': 'text/xml',
                    'content-length': '4792'
                },
                'RetryAttempts': 0
            }
        }
        '''

        if not self.IsSqsEvent(obj):
            return []

        ret = []
        for msg in ret['Messages']:
            body = self.FromJson(msg['Body'])
            struct = self.STRUCT(body)
            ret.append(struct)

        return ret