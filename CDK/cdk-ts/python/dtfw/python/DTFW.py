# 📚 DTFW

def test():
    return 'this is a DTFW test.'


class DTFW:
    
  
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
        if not self._graph: 
            from GRAPH import GRAPH as proxy
            self._graph = proxy()
        return self._graph
    

    def Host(self):
        if not self._host: 
            from HOST import HOST as proxy
            self._host = proxy()
        return self._host
    

    def Item(self, item):
        from ITEM import ITEM as proxy
        return proxy(item)
    

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
    

    def Vault(self):
        from VAULT import VAULT as proxy
        return proxy()
    

    def Web(self):
        from WEB import WEB as proxy
        return proxy()