# 📚 DTFW

# 👉 https://stackoverflow.com/questions/24853923/type-hinting-a-collection-of-a-specified-type
from typing import List, Set, Tuple, Dict
from AWS import AWS
from UTILS import UTILS


def test():
    return 'this is a DTFW test.'


# ✅ DONE
class DTFW(AWS, UTILS):
    ''' 👉 https://quip.com/z095AywlrA82/-Domain-Trust-Framework '''
    

    def Broker(self):
        ''' 👉 https://quip.com/SJadAQ8syGP0/-Broker '''
        if not self._broker: 
            from BROKER import BROKER as proxy
            self._broker = proxy()
        return self._broker

    
    def Code(self, item: any):
        from CODE import CODE as proxy
        return proxy(item)
    

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
    

    def Subscriber(self):
        from SUBSCRIBER import SUBSCRIBER as proxy
        return proxy()
    

    def SyncApi(self):
        from SYNCAPI import SYNCAPI as proxy
        return proxy()
    

    def Utils(self):
        from UTILS import UTILS as proxy
        return proxy()
    

    def Vault(self):
        from VAULT import VAULT as proxy
        return proxy()
    

    