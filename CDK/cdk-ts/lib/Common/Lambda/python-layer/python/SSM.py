# 📚 SSM

import boto3


def test():
    return 'this is a SSM test.'


ssm = boto3.client('ssm')
class SSM:

    
    def Get(self, name: str) -> str:
        return ssm.get_parameter(Name=name)['Parameter']['Value']

    
    def Set(self, name: str, value: str):
        ssm.put_parameter(Name=name, Value=value, Type="String")


    def Delete(self, name: str):
        ssm.delete_parameter(Name=name)