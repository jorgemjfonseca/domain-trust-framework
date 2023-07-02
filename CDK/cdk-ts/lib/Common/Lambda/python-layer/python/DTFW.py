import boto3
import os
import json


def test():
    return 'this is a DTFW test.'


class DTFW:
    
  
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