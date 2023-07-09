# 📚 BROKER_BINDS

# 👉 https://stackoverflow.com/questions/24853923/type-hinting-a-collection-of-a-specified-type
from typing import List, Set, Tuple, Dict
from BROKER_SESSIONS import BROKER_SESSIONS

from BROKER_SETUP import BROKER_SETUP
from DTFW import DTFW
from MSG import MSG


class BROKER_BINDS(BROKER_SESSIONS, BROKER_SETUP, DTFW):
    ''' 👉 https://quip.com/oSzpA7HRICjq/-Broker-Binds '''

    
    # ✅ DONE
    def Binds(self):
        ''' 👉 https://quip.com/oSzpA7HRICjq#temp:C:DSDcace3164ba9e44608c1a16cb1 '''
        return self.DYNAMO('BINDS', keys=['WalletID', 'Vault', 'Code'])
    

    # ✅ DONE
    def Vaults(self):
        ''' 👉 https://quip.com/oSzpA7HRICjq#temp:C:DSD1ead4d286ae34b40a565e308c '''
        return self.DYNAMO('VAULTS', keys=['WalletID', 'Vault'])
    
    
    def HandleBindable(self, event):
        ''' 🐌 https://quip.com/oSzpA7HRICjq#temp:C:DSD2aa2718d92bf4941ac7bb41e9 
        "Body": {
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",
            "Binds": [{
                "Code": "iata.org/SSR/WCHR"
            }]
        }
        '''
        msg = self.MSG(event)

        session = self.Sessions().Require(msg)
        wallet = self.Wallets().Require(session)
        language = wallet.Require('Language')
    
        codes = [bind.Require('Code') for bind in msg.Structs('Binds')]

        ret = self.GRAPH().InvokeTranslate(
            language= language,
            codes= codes
        )
        ''' 🏃 https://quip.com/hgz4A3clvOes#temp:C:bDA9d34010d13574c2f95fe4de54 
        {
            "Language": "pt-br",
            "Domains": [{
                "Domain": "example.com",
                "Translation": "Example Airlines"
            }],
            "Codes": [{
                "Code": "iata.org/SSR/WCHR",
                "Translation": "Wheelchair assistance required"
            }]
        }
        '''

        ''' 🐌 https://quip.com/PCunAKUqSObO/-Notifier#temp:C:UKEe59fd4b4d73345348afd67d5f '''
        bindable = {
            "WalletID": wallet.ID(),
            "SessionID": session.ID(),
            "Codes": [
                {
                    "Code": "iata.org/SSR/WCHR",
                    "Translation": "Wheelchair assistance required; passenger can walk short distance up or down stairs."
                }
            ]
        }

        session.Att('Bindabale')


    
    # ✅ DONE
    def HandleBinds(self, event):
        ''' 🚀 https://quip.com/oSzpA7HRICjq#temp:C:DSD0d59568b34f74ef0a2df28896 '''
        '''
        "Body": {
          "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a"
        }
        '''
        msg = self.MSG(event)

        wallet = self.Wallets().Get(msg)
        wallet.Require()      

        '''
        {
            "Vaults": [{
                "Vault": "iata.org",
                "Translation": "IATA",
                "Binds": [{
                    "BindID": "793af21d-12b1-4cea-8b55-623a19a28fc5",
                    "Code": "iata.org/SSR/WCHR",
                    "Translation": "Wheelchair for ramp"
                }]
            }],
        }
        '''
        return { 
            'Hosts': wallet.Att('Vaults', default=[])
        }   


    # ✅ DONE
    def InvokeBound(self, source:str, to:str, walletID:str, binds:List[object], request:MSG):
        ''' 🏃 Broker.Bound: 🐌 https://quip.com/oSzpA7HRICjq/-Broker-Binds#temp:C:DSD3f7309f961e24f0ebb5897e2f '''        

        self.MESSENGER().Push(
            source= source,
            to= to,
            body= {
                "WalletID": walletID,
                "Request": request.Body(),
                "Binds": binds
            })


    def HandleBound(self, event):
        ''' 🐌 https://quip.com/oSzpA7HRICjq/-Broker-Binds#temp:C:DSD3f7309f961e24f0ebb5897e2f '''
        '''
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "Request": {...},
            "Binds": [{
                "BindID": "793af21d-12b1-4cea-8b55-623a19a28fc5",
                "Code": "iata.org/SSR/WCHR"
            }]
        }
        '''
        self.MSG(event)


    def HandleUnbind(self, event):
        ''' 🐌 https://quip.com/oSzpA7HRICjq#temp:C:DSDcd716c71b51c4c528a8c218fd '''
        '''
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "BindID": "793af21d-12b1-4cea-8b55-623a19a28fc5"
        }
        '''
        self.MSG(event)
