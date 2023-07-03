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

