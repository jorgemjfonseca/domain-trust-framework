import boto3


def test():
    return 'this is a SECRETS test.'


secretsmanager = boto3.client('secretsmanager')
class SECRETS:

    @staticmethod
    def Get(secretId):
        return secretsmanager.get_secret_value(
            SecretId= secretId
        )['SecretString']

