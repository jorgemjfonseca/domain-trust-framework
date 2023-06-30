# ManifesterBucket-ViewerFn

import json
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


appconfig = boto3.client('appconfigdata')
def read_app_config():
    
    session = appconfig.start_configuration_session(
        ApplicationIdentifier=os.environ['CONFIG_APP'],
        EnvironmentIdentifier=os.environ['CONFIG_ENV'],
        ConfigurationProfileIdentifier=os.environ['CONFIG_PROFILE'],
        RequiredMinimumPollIntervalInSeconds=60
    )
    token = session['InitialConfigurationToken']
    
    config = appconfig.get_latest_configuration(
        ConfigurationToken=token
    )
    value = config['Configuration'].read()
    return value


def handler(event, context):

    yaml_data = read_app_config()

    # Return a response
    return {
        'statusCode': 200,
        'body': yaml_data,
        "headers": {
            "content-type": "text/yaml"
        }
    }
