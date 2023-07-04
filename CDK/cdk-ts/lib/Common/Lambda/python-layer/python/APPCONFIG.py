# 📚 APPCONFIG

import boto3
import os


def test():
    return 'this is a APPCONFIG test.'


appconfig = boto3.client('appconfigdata')
class APPCONFIG:
        

    def Get(
        self,    
        CONFIG_APP: str = 'CONFIG_APP', 
        CONFIG_ENV: str = 'CONFIG_ENV', 
        CONFIG_PROFILE: str = 'CONFIG_PROFILE'
    ) -> str:
    
        app = os.environ[CONFIG_APP]
        print(f'{app=}')
        
        env = os.environ[CONFIG_ENV]
        print(f'{env=}')
        
        profile = os.environ[CONFIG_PROFILE]
        print(f'{profile=}')
        
        session = appconfig.start_configuration_session(
            ApplicationIdentifier=app,
            EnvironmentIdentifier=env,
            ConfigurationProfileIdentifier=profile,
            RequiredMinimumPollIntervalInSeconds=60
        )
        token = session['InitialConfigurationToken']
        
        config = appconfig.get_latest_configuration(
            ConfigurationToken=token
        )
        value = config['Configuration'].read()
        return value

