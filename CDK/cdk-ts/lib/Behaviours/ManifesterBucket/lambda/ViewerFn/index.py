# ManifesterBucket-ViewerFn

import boto3
import os

s3 = boto3.client('s3')
def read_s3():
    bucket_name = os.environ['BUCKET_NAME']
    object_key = os.environ['FILE_NAME']

    # Retrieve the S3 object
    response = s3.get_object(Bucket=bucket_name, Key=object_key)

    # Read the data
    yaml_data = response['Body'].read().decode('utf-8')
    
    return yaml_data


def handler(event, context):

    from MANIFEST import MANIFEST
    manifest = MANIFEST.FromAppConfig()
    
    from UTILS import UTILS
    return UTILS.HttpResponse(body=manifest, format='yaml')
