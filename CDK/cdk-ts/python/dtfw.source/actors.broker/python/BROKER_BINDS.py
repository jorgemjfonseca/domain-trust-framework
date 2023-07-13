# 📚 BROKER_BINDS

# 👉 https://stackoverflow.com/questions/24853923/type-hinting-a-collection-of-a-specified-type
from typing import List, Set, Tuple, Dict
from BIND import BIND
from BROKER_SESSIONS import BROKER_SESSIONS

from BROKER_SETUP import BROKER_SETUP
from BROKER_BASE import BROKER_BASE
from DTFW import DTFW
from MSG import MSG
from STRUCT import STRUCT
from WALLET import WALLET


# ✅ DONE
class BROKER_BINDS(BROKER_SETUP, BROKER_BASE):
    ''' 👉 https://quip.com/oSzpA7HRICjq/-Broker-Binds '''

    
    # ✅ DONE
    def InvokeBindable(self, to:str, source:str, sessionID:str, codes:List[str]):
        '''
        "Body": {
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",
            "Codes": ["iata.org/SSR/WCHR"]
        }'''
        self.MESSENGER().Push(
            to= to,
            source= source, 
            subject= 'Bindable@Broker',
            body= {
                "SessionID": sessionID,
                "Codes": codes
            }
        )


    # ✅ DONE
    def HandleBindable(self, event):
        ''' 🗄️🐌 https://quip.com/oSzpA7HRICjq#temp:C:DSD2aa2718d92bf4941ac7bb41e9 
        "Body": {
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",
            "Codes": ["iata.org/SSR/WCHR"]
        }
        '''
        msg = self.MSG(event)

        session = self.GetSession(msg)
        session.MatchHost(msg)

        wallet = self.GetWallet(session)
    
        translation = self.GRAPH().InvokeTranslate(
            language= wallet.Language(),
            codes= msg.Require('Codes')
        )

        bindable = translation.Require('Codes')
        session.Bindable(bindable)

        ''' 🐌 https://quip.com/PCunAKUqSObO/-Notifier#temp:C:UKEe59fd4b4d73345348afd67d5f '''
        self.NOTIFIER().InvokeBindable(
            source= 'Bindable@Broker',
            wallet= wallet,
            session= session, 
            codes= bindable
        )

    
    # ✅ DONE
    def HandleBinds(self, event):
        ''' 🚀 https://quip.com/oSzpA7HRICjq#temp:C:DSD0d59568b34f74ef0a2df28896 
        "Body": {}
        '''
        msg, wallet = self.VerifyWalletSignature(event)

        return { 
            "Binds": [
                {
                    "ID": bind.ID(),
                    "Vault": bind.VaultDomain(),
                    "VaultTitle": bind.VaultTranslation(),
                    "Code": bind.CodeCode(),
                    "CodeTitle": bind.CodeTranslation()
                }
                for bind in self.BindsOf(wallet) 
            ]
        }
    

    # ✅ DONE
    def HandleBind(self, event):
        ''' 🧑‍🦰🐌 https://quip.com/IZapAfPZPnOD#temp:C:PDZf81764583b31439f999550159 
        "Body": {
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",
            "Codes": ["iata.org/SSR/WCHR"]
        }
        '''
        msg, wallet = self.VerifyWalletSignature(event)
        session = self.GetSession(msg)
        session.MatchWalletID(msg)
        
        binds: List[BIND] = []
        for code in msg.List('Codes'):
            bindable = session.Bindable().Where('Code', equals=code)
            bind = {
                "ID": self.UUID(),
                "WalletID": wallet.ID(),
                "Vault": session.HostObject(),
                "Code": bindable
            }
            
            self.Binds().Insert(bind)
            binds.append(bind)
 
        # Notify the vault about the new binds.
        self.VAULT().InvokeBound(
            source= 'Bind@Broker',
            vault= session.HostDomain(),
            sessionID= session.ID(), 
            publicKey= wallet.PublicKey(),
            binds= [
                {
                    "ID": bind['ID'],
                    "Code": bind['Code']['Code']
                }
                for bind in binds
            ]
        )
                
        # Notify the UI about the new binds.
        self.NOTIFIER().InvokeBound(
            wallet= wallet,
            source= 'Bind@Broker',
            bind= binds)
        
        # Alert the UI to refresh the binds list.
        self.NOTIFIER().InvokeUpdated(
            source= 'Bind@Broker',
            wallet= wallet,
            updates= ['BINDS'],
        )
        

    # ✅ DONE
    def HandleUnbind(self, event):
        ''' 🧑‍🦰🐌 https://quip.com/oSzpA7HRICjq#temp:C:DSDcd716c71b51c4c528a8c218fd 
        "Body": {
            "BindID": "793af21d-12b1-4cea-8b55-623a19a28fc5"
        }
        '''
        msg, wallet = self.VerifyWalletSignature(event)
        bind = self.GetBind(msg)
        bind.MatchWalletID(msg)

        self.VAULT().InvokeUnbind(
            source= 'Unbind@Broker',
            vault= bind.VaultDomain(),
            bindID= bind.ID()
        )

        # Alert the UI to refresh the binds list.
        self.NOTIFIER().InvokeUpdated(
            source= 'Unbind@Broker',
            wallet= wallet,
            updates= ['BINDS'],
        )
