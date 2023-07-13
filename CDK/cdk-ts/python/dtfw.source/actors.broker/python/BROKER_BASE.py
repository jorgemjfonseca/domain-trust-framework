# 📚 BROKER

# https://stackoverflow.com/questions/48709104/how-do-i-specify-multiple-types-for-a-parameter-using-type-hints
from typing import Union

import string
import random
from BIND import BIND
from CREDENTIAL import CREDENTIAL
from DTFW import DTFW
from MSG import MSG
from SESSION import SESSION
from WALLET import WALLET


# ✅ DONE
class BROKER_BASE(DTFW):
    

    # ✅ DONE
    def VerifyWalletSignature(self, event):
        msg = self.MSG(event)
        walletID = msg.From()
        wallet = self.GetWallet(walletID)
        wallet.VerifySignature(msg)
        return msg, wallet
    

    # ✅ DONE
    def Domain(self) -> str:
        return self.Environment('DOMAIN')
    
    
    # ✅ DONE
    def Wallets(self): 
        return self.DYNAMO('WALLETS')
    

    # ✅ DONE
    def GetWallet(self, walletID: Union[str,SESSION]):
        if isinstance(walletID, SESSION):
            walletID = walletID.WalletID()
        return WALLET(self.Wallets().Get(walletID))
    

    # ✅ DONE
    def Sessions(self): 
        return self.DYNAMO('SESSIONS')
    
    
    # ✅ DONE
    def GetSession(self, sessionID: Union[str,MSG]):
        if isinstance(sessionID, MSG):
            sessionID = MSG.Require('SessionID')
        return SESSION(self.Sessions().Require(sessionID))
    

    # ✅ DONE
    def SessionsOf(self, wallet:WALLET): 
        items = self.Sessions().Query('WalletID', equals=wallet.ID())
        return SESSION.FromItems(items)
    

    # ✅ DONE
    def Binds(self):
        return self.DYNAMO('BINDS')
    

    # ✅ DONE
    def GetBind(self, bindID: Union[str, MSG]):
        if isinstance(bindID, MSG):
            bindID = bindID.Require['BindID']
        return BIND(self.Binds().Require(bindID))
        

    # ✅ DONE
    def BindsOf(self, wallet:WALLET=None):
        items = self.Binds().Query('WalletID', equals=wallet.ID())
        return BIND.FromItems(items)
    

    # ✅ DONE
    def Credentials(self, wallet:WALLET=None): 
        return self.DYNAMO('CREDENTIALS')
    
    
    # ✅ DONE
    def GetCredential(self, credentialID):
        return CREDENTIAL(self.Credentials().Require(credentialID))


    # ✅ DONE
    def CredentialsOf(self, wallet:WALLET=None): 
        items = self.Credentials().Query('WalletID', equals=wallet.ID())
        return CREDENTIAL.FromItems(items)
    

    