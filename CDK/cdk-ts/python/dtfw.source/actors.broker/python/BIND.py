# 📚 BIND

# 👉 https://stackoverflow.com/questions/33533148/how-do-i-type-hint-a-method-with-the-type-of-the-enclosing-class
from __future__ import annotations

# 👉 https://stackoverflow.com/questions/24853923/type-hinting-a-collection-of-a-specified-type
from typing import List, Set, Tuple, Dict, Union

from ITEM import ITEM
from MSG import MSG


class BIND(ITEM):
    ''' 🪣 https://quip.com/oSzpA7HRICjq#temp:C:DSDcace3164ba9e44608c1a16cb1 
    {    
        "ID": "793af21d-12b1-4cea-8b55-623a19a28fc5",
        "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
        "Vault": {
            "Domain": "iata.org",
            "Translation": "IATA"
        },
        "Code": {
            "Code": "iata.org/SSR/WCHR",
            "Translation": "Wheelchair for ramp"
        }
    }
    '''

    def FromItems(items:List[ITEM]) -> List[BIND]:
        ret = []
        for item in items:
            ret.append(BIND(item))
        return ret
    

    def CodeCode(self):
        return self.RequireStr('Code.Code')
    
    
    def VaultDomain(self):
        return self.RequireStr('Vault.Domain')
    

    def VaultTranslation(self, set=str):
        return self.RequireStr('Vault.Translation', set=set)
    

    def CodeTranslation(self, set=str):
        return self.RequireStr('Code.Translation', set=set)
    

    def MatchWalletID(self, walletID:Union[str,MSG]):
        if isinstance(walletID, MSG):
            walletID = walletID.From()
        return self.Match('WalletID', walletID)