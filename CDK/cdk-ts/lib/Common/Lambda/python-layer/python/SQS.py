import boto3
import os
import json



def test():
    return 'this is a SQS test.'



sqs = boto3.client("sqs")
class SQS:
    

    def __init__(self, alias):
        name = os.environ[alias]
        self.url = sqs.get_queue_url(QueueName= name)
        

    def Send(self, msg):
        resp = sqs.send_message(
            QueueName= self.url,
            MessageBody= json.dumps(msg)
        )
        code = resp['ResponseMetadata']['HTTPStatusCode']
        if code != 200:
            raise Exception('Error sending to the queue.')
        return resp
    
