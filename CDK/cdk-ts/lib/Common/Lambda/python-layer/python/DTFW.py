# 📚 DTFW

def test():
    return 'this is a DTFW test.'


class DTFW:
    
  
    def RegisterDomain(self, hosted_zone_id):
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


    def Sqs(self, alias:str):
        from SQS import SQS as proxy
        return proxy(alias)
    

    def Dynamo(self, alias:str=None):
        from DYNAMO import DYNAMO as proxy
        return proxy(alias)
    

    def Msg(self, event:any = {}):
        from MSG import MSG as proxy
        return proxy(event)
    

    def Manifest(self, manifest:any = None):
        from MANIFEST import MANIFEST as proxy
        return proxy(manifest)
    

    def Messenger(self):
        from MESSENGER import MESSENGER as proxy
        return proxy()
    

    def Domain(self, name:str):
        from DOMAIN import DOMAIN as proxy
        return proxy(name)
    

    def Utils(self):
        from UTILS import UTILS as proxy
        return proxy()
    

    def Code(self, item: any):
        from CODE import CODE as proxy
        return proxy(item)
    

    def Subscriber(self):
        from SUBSCRIBER import SUBSCRIBER as proxy
        return proxy()
    

    def Bus(self):
        from BUS import BUS as proxy
        return proxy()
    
    
    def SyncApi(self):
        from SYNCAPI import SYNCAPI as proxy
        return proxy()
    
    
    def Publisher(self):
        from PUBLISHER import PUBLISHER as proxy
        return proxy()
    
    
    def Lambda(alias: str=None):
        from LAMBDA import LAMBDA as proxy
        return proxy(alias)
    

    def AppConfig():
        from APPCONFIG import APPCONFIG as proxy
        return proxy()
    

    def Web():
        from WEB import WEB as proxy
        return proxy()