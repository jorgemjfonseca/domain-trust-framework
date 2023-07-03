# 📚 DTFW

def test():
    return 'this is a DTFW test.'


class DTFW:
    
  
    def AppConfig(self):
        from APPCONFIG import APPCONFIG as proxy
        return proxy()
        
    
    def Bus(self):
        from BUS import BUS as proxy
        return proxy()
    
    
    def Code(self, item: any):
        from CODE import CODE as proxy
        return proxy(item)
    

    def Dynamo(self, alias:str=None):
        from DYNAMO import DYNAMO as proxy
        return proxy(alias)
    
    
    def Domain(self, name:str=None):
        from DOMAIN import DOMAIN as proxy
        return proxy(name)
    

    def Graph(self):
        from GRAPH import GRAPH as proxy
        return proxy()
    

    def Lambda(self, alias: str=None):
        from LAMBDA import LAMBDA as proxy
        return proxy(alias)


    def Listener(self):
        from LISTENER import LISTENER as proxy
        return proxy()
    

    def Manifest(self, manifest:any = None):
        from MANIFEST import MANIFEST as proxy
        return proxy(manifest)
    

    def Manifester(self):
        from MANIFESTER import MANIFESTER as proxy
        return proxy()
    

    def Messenger(self):
        from MESSENGER import MESSENGER as proxy
        return proxy()


    def Msg(self, event:any = {}):
        from MSG import MSG as proxy
        return proxy(event)
    

    def Publisher(self):
        from PUBLISHER import PUBLISHER as proxy
        return proxy()
    

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
    

    def Subscriber(self):
        from SUBSCRIBER import SUBSCRIBER as proxy
        return proxy()
    

    def SyncApi(self):
        from SYNCAPI import SYNCAPI as proxy
        return proxy()
    

    def Timer(self):
        from TIMER import TIMER as proxy
        return proxy()
    

    def Utils(self):
        from UTILS import UTILS as proxy
        return proxy()
    

    def Web(self):
        from WEB import WEB as proxy
        return proxy()