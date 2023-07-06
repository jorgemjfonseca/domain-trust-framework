# 📚 DTFW

# 👉 https://stackoverflow.com/questions/24853923/type-hinting-a-collection-of-a-specified-type
from typing import List, Set, Tuple, Dict

def test():
    return 'this is a DTFW test.'


class DTFW:
    ''' 👉 https://quip.com/z095AywlrA82/-Domain-Trust-Framework '''
    
  
    def AppConfig(self):
        if not self._appConfig: 
            from APPCONFIG import APPCONFIG as proxy
            self._appConfig = proxy()
        return self._appConfig
        

    def Broker(self):
        ''' 👉 https://quip.com/SJadAQ8syGP0/-Broker '''
        if not self._broker: 
            from BROKER import BROKER as proxy
            self._broker = proxy()
        return self._broker


    def Bus(self):
        if not self._bus: 
            from BUS import BUS as proxy
            self._bus = proxy()
        return self._bus
    
    
    def Code(self, item: any):
        from CODE import CODE as proxy
        return proxy(item)
    

    def Dynamo(self, alias:str=None, keys:List[str]=None):
        from DYNAMO import DYNAMO as proxy
        return proxy(alias=alias, keys=keys)
    
    
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
    

    def Struct(self, item):
        from STRUCT import STRUCT as proxy
        return proxy(item)
    

    def Unstruct(self, obj: any):
        from UTILS import UTILS as proxy
        return proxy.Unstruct(obj)
    

    def Lambda(self, alias: str=None):
        from LAMBDA import LAMBDA as proxy
        return proxy(alias)


    def Listener(self):
        if not self._listener:
            from LISTENER import LISTENER as proxy
            self._listener = proxy()
        return self._listener
    

    def Manifest(self, manifest:any = None):
        from MANIFEST import MANIFEST as proxy
        return proxy(manifest)
    

    def Manifester(self):
        if not self._manifester:
            from MANIFESTER import MANIFESTER as proxy
            self._manifester = proxy()
        return self._manifester
    

    def Messenger(self):
        ''' 👉 Messagenger behaviour of a domain. '''
        if not self._messenger:
            from MESSENGER import MESSENGER as proxy
            self._messenger = proxy()
        return self._messenger


    def Msg(self, event:any = {}):
        ''' 👉 Structure of a message: { Header, Body, Hash, Signature }. '''
        from MSG import MSG as proxy
        return proxy(event)
    

    def Wrap(self, to:str=None, body:any=None):
        ''' 👉 Returns a stamped message, with header and body. '''
        from MSG import MSG as proxy
        return proxy.Wrap(to= to, body= body)


    def Notifier(self):
        if not self._notifier:
            from NOTIFIER import NOTIFIER as proxy
            self._notifier = proxy()
        return self._notifier
    

    def Publisher(self):
        if not self._publisher:
            from PUBLISHER import PUBLISHER as proxy
            self._publisher = proxy()
        return self._publisher
    

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