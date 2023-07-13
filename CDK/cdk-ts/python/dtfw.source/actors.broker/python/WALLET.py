# 📚 WALLET

# 👉 https://stackoverflow.com/questions/24853923/type-hinting-a-collection-of-a-specified-type
from typing import List, Set, Tuple, Dict

from ITEM import ITEM
from STRUCT import STRUCT
from MSG import MSG


class WALLET(ITEM):
    ''' 🪣 https://quip.com/zaYoA4kibXAP/-Broker-Setup#temp:C:DQN5a1b1a16ec7f4a29907cd1215
    {    
        "ID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
        "Language": "en-us",
        "PublicKey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDH+wPrKYG1KVlzQUVtBghR8n9dzcShSZo0+3KgyVdOea7Ei7vQ1U4wRn1zlI5rSqHDzFitblmqnB2anzVvdQxLQ3UqEBKBfMihnLgCSW8Xf7MCH+DSGHNvBg2xSNhcfEmnbLPLnbuz4ySn1UB0lH2eqxy50zstxhTY0binD9Y+rwIDAQAB",
        "Notifier": "any-wallet.com"
    }
    '''

    def VerifySignature(self, msg: MSG):
        self.Require()
        publicKey = self.Require('PublicKey')
        msg.VerifySignature(publicKey)


    def ID(self):
        return self.Require('WalletID')


    def Notifier(self):
        return self.Require('Notifier')


    def Language(self):
        return self.Require('Language')
    

    def PublicKey(self):
        return self.Require('PublicKey')