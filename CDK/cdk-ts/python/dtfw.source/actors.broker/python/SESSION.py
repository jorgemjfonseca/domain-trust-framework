# 📚 SESSION

# 👉 https://stackoverflow.com/questions/33533148/how-do-i-type-hint-a-method-with-the-type-of-the-enclosing-class
from __future__ import annotations

# 👉 https://stackoverflow.com/questions/24853923/type-hinting-a-collection-of-a-specified-type
from typing import List, Set, Tuple, Dict, Union

from ITEM import ITEM
from STRUCT import STRUCT
from MSG import MSG
from DTFW import DTFW


class SESSION(ITEM, DTFW):
    ''' 🪣 https://quip.com/HrgkAuQCqBez#temp:C:bXDdd6c1585433f4b6495262e8df 
    {   
        "ID": "125a5c75-cb72-43d2-9695-37026dfcaa48",
        "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
        "SessionTime": "2018-12-10T13:45:00.000Z",
        "Host": {
            "Domain": "iata.org",
            "Translation": "IATA"
        },    
        "Vaults": [
            "one.amazon.com",
            "any-profile.com",
            "nhs.uk"
        ],
        "Bindable": [{
            "Code": "...",
            "Translation": "..."
        }]
    }'''


    def FromItems(items:List[ITEM]) -> List[SESSION]:
        ret = []
        for item in items:
            ret.append(SESSION(item))
        return ret


    def HostObject(self):
        return self.Require('Host')

    
    def HostDomain(self):
        return self.RequireStr('Host.Domain')
    

    def HostTranslation(self, set=str):
        return self.RequireStr('Host.Translation', set=set)
    

    def SessionTime(self):
        return self.RequireStr('SessionTime')
    

    def WalletID(self):
        return self.RequireStr('WalletID')


    def MatchHost(self, host:Union[str,MSG]):
        if isinstance(host, MSG):
            host = host.From()
        return self.Match('Host.Domain', host)
    

    def MatchWalletID(self, walletID:Union[str,MSG]):
        if isinstance(walletID, MSG):
            walletID = walletID.From()
        return self.Match('WalletID', walletID)
    

    def Abandon(self, source:str):
        ''' Call 🐌 Abandoned: 🤗 Host on the host '''
        self.HOST().InvokeAbandoned(
            source= source,
            to= self.HostDomain(),
            sessionID= self.ID
        )


    def SuppressVaults(self, source:str):
        # 🪣 https://quip.com/rKzMApUS5QIi/-Broker-Share#temp:C:WTI65d339805abc4a79afae419df
        # For every vault in 🪣 Queries: 🤵📎 Broker.Share():
            # where session’s match
            # call 🐌 Suppress: 🗄️ Vault
        for vault in self.List['Vaults']:
            self.VAULT().InvokeSuppress(
                to= vault,
                consumer= self.HostDomain(),
                sessionID= self.ID(),
                source= source
            )


    def Bindable(self, set=None):
        if set != None:
            self.Att('Bindable', set=set)
            self.Update()
        return self.Struct('Bindable')
