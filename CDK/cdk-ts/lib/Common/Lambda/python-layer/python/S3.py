import boto3
import os


def test():
    return 'this is a S3 test.'


s3 = boto3.client('s3')
class S3:
    
    def GetText(
        bucket_name = os.environ['BUCKET_NAME'],
        object_key = os.environ['FILE_NAME']
    ) -> str:
        
        # Retrieve the S3 object
        response = s3.get_object(Bucket=bucket_name, Key=object_key)

        # Read the data
        text = response['Body'].read().decode('utf-8')
        
        return text
    
