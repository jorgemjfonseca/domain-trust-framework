# 📚 LAMBDA

import boto3
import os
import json



def test():
    return 'this is a LAMBDA test.'


lambdaClient = boto3.client('lambda')
class LAMBDA:

    def __init__(self, alias):
        if alias:
            self.name = os.environ[alias]


    # 👉 https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/client/invoke.html
    def Invoke(self, params:any):
        print(f'invoking [{self.name}]({params})...')
        
        response = lambdaClient.invoke(
            FunctionName = self.name,
            Payload=json.dumps(params),
            LogType='Tail')
        
        returned = json.loads(response['Payload'].read())
        print(f'{returned=}')
        return returned

