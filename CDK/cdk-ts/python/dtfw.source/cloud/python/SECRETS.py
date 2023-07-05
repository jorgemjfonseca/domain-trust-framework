# 📚 SECRETS

import boto3


def test():
    return 'this is a SECRETS test.'


secretsmanager = boto3.client('secretsmanager')
class SECRETS:

    
    def Get(self, secretId):
        return secretsmanager.get_secret_value(
            SecretId= secretId
        )['SecretString']


    def Set(self, name, value):
        print(f'{name=}')
        print(f'{value=}')
        
        try:
            secretsmanager.create_secret(
                Name=name,
                SecretString=value
            )
        except:
            secretsmanager.update_secret(
                SecretId=name,
                SecretString=value
            )