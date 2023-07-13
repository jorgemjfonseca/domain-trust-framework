# 📚 CREDENTIAL

# 👉 https://stackoverflow.com/questions/33533148/how-do-i-type-hint-a-method-with-the-type-of-the-enclosing-class
from __future__ import annotations

# 👉 https://stackoverflow.com/questions/24853923/type-hinting-a-collection-of-a-specified-type
from typing import List, Set, Tuple, Dict

from ITEM import ITEM


class CREDENTIAL(ITEM):
    ''' 🪣 https://quip.com/sN8DACFLN9wM#temp:C:AfTbbe653b5e8ad4f38b44dc8e7d
    {
        "ID": "7bcf138b-db79-4a42-9d36-2655f8ff1f7c",
        "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
        "Issuer": {
            "Domain": "nhs.uk",
            "Translation": "Wheelchair for ramp"
        },
        "Code": {
            "Code": "iata.org/SSR/WCHR",
            "Title": "Wheelchair credential"
        },
        "Path": "/storage/tf/creds/nhs.uk/7bcf138b-db79-4a42-9d36-2655f8ff1f7c"
    }'''
    

    def FromItems(items:List[ITEM]) -> List[CREDENTIAL]:
        ret = []
        for item in items:
            ret.append(CREDENTIAL(item))
        return ret


    def IssuerDomain(self):
        return self.RequireStr('Issuer.Domain')
    

    def CodeCode(self):
        return self.RequireStr('Code.Code')
    
    
    def IssuerTranslation(self, set=str):
        return self.RequireStr('Issuer.Translation', set=set)
    

    def CodeTranslation(self, set=str):
        return self.RequireStr('Code.Translation', set=set)