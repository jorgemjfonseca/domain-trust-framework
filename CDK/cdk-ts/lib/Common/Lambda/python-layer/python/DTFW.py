import boto3
import os
import json


def test():
    return 'this is a DTFW test.'


class DTFW:
    
  
    @staticmethod
    def RegisterDomain(hosted_zone_id):
        ''' 👉 host -t NS 105b4478-eaa5-4b73-b2a5-4da2c3c2dac0.dev.dtfw.org '''
        print(f'register_domain')

        from ROUTE53 import ROUTE53
        from WEB import WEB

        zone = ROUTE53(hosted_zone_id)

        domain = zone.Domain()
        serverList = zone.NameServerList()
        dnsSec = zone.DX()
        dtfwOrg = 'z6jsx3ldteaiewnhm4dwuhljzi0vrxgn.lambda-url.us-east-1.on.aws'

        url = f'https://{dtfwOrg}/?domain={domain}&servers={serverList}&dnssec={dnsSec}'
        WEB.Get(url)


    @staticmethod
    def SQS(alias:str):
        from SQS import SQS as proxy
        return proxy(alias)
    

    @staticmethod
    def DYNAMO(alias:str):
        from DYNAMO import DYNAMO as proxy
        return proxy(alias)
    

    @staticmethod
    def MSG(event:any = {}):
        from MSG import MSG as proxy
        return proxy(event)
    

    @staticmethod
    def MANIFEST(manifest:any = None):
        from MANIFEST import MANIFEST as proxy
        return proxy(manifest)
    

    @staticmethod
    def DOMAIN(domainName:str):
        from DOMAIN import DOMAIN as proxy
        return proxy(domainName)