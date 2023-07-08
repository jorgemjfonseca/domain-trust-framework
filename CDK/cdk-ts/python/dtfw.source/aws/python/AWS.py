# 📚 AWS

# 👉 https://stackoverflow.com/questions/24853923/type-hinting-a-collection-of-a-specified-type
from typing import List, Set, Tuple, Dict


class AWS:
    ''' 👉 https://quip.com/z095AywlrA82/-Domain-Trust-Framework '''
    
  
    def APPCONFIG(self):
        if not self._appConfig: 
            from APPCONFIG import APPCONFIG as proxy
            self._appConfig = proxy()
        return self._appConfig


    def BUS(self):
        if not self._bus: 
            from BUS import BUS as proxy
            self._bus = proxy()
        return self._bus
    

    def DYNAMO(self, alias:str=None, keys:List[str]=None):
        ''' 👉 DynamoDB table manager. '''
        from DYNAMO import DYNAMO as proxy
        return proxy(alias=alias, keys=keys)
    

    def LAMBDA(self, alias: str=None):
        from LAMBDA import LAMBDA as proxy
        return proxy(alias)
    

    def ROUTE53(self, hosted_zone_id: str):
        from ROUTE53 import ROUTE53 as proxy
        return proxy(hosted_zone_id)
    

    def S3(self):
        from S3 import S3 as proxy
        return proxy()
    

    def SECRETS(self):
        from SECRETS import SECRETS as proxy
        return proxy()


    def SQS(self, alias:str=None):
        from SQS import SQS as proxy
        return proxy(alias)
    

    def SSM(self):
        from SSM import SSM as proxy
        return proxy()
