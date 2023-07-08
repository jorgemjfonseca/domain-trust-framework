# 📚 AWS

# 👉 https://stackoverflow.com/questions/24853923/type-hinting-a-collection-of-a-specified-type
from typing import List, Set, Tuple, Dict


class AWS:
    ''' 👉 https://quip.com/z095AywlrA82/-Domain-Trust-Framework '''
    
  
    def AppConfig(self):
        if not self._appConfig: 
            from APPCONFIG import APPCONFIG as proxy
            self._appConfig = proxy()
        return self._appConfig


    def Bus(self):
        if not self._bus: 
            from BUS import BUS as proxy
            self._bus = proxy()
        return self._bus
    

    def Dynamo(self, alias:str=None, keys:List[str]=None):
        from DYNAMO import DYNAMO as proxy
        return proxy(alias=alias, keys=keys)
    

    def Lambda(self, alias: str=None):
        from LAMBDA import LAMBDA as proxy
        return proxy(alias)
    

    def Route53(self, hosted_zone_id: str):
        from ROUTE53 import ROUTE53 as proxy
        return proxy(hosted_zone_id)
    

    def S3(self):
        from S3 import S3 as proxy
        return proxy()
    

    def Secrets(self):
        from SECRETS import SECRETS as proxy
        return proxy()


    def Sqs(self, alias:str):
        from SQS import SQS as proxy
        return proxy(alias)
    

    def Ssm(self):
        from SSM import SSM as proxy
        return proxy()
