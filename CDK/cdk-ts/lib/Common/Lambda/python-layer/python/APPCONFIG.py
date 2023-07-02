import boto3
import os

def test():
    return 'this is a APPCONFIG test.'


appconfig = boto3.client('appconfigdata')
class APPCONFIG:
        
    @staticmethod
    def Get(
        CONFIG_APP: str = 'CONFIG_APP', 
        CONFIG_ENV: str = 'CONFIG_ENV', 
        CONFIG_PROFILE: str = 'CONFIG_PROFILE'
    ) -> str:
    
        session = appconfig.start_configuration_session(
            ApplicationIdentifier=os.environ[CONFIG_APP],
            EnvironmentIdentifier=os.environ[CONFIG_ENV],
            ConfigurationProfileIdentifier=os.environ[CONFIG_PROFILE],
            RequiredMinimumPollIntervalInSeconds=60
        )
        token = session['InitialConfigurationToken']
        
        config = appconfig.get_latest_configuration(
            ConfigurationToken=token
        )
        value = config['Configuration'].read()
        return value

