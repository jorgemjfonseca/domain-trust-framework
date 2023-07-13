# 📚 VAULT

def test():
    return 'this is VAULT test.'

from typing import List, Set, Tuple, Dict, Union
from HANDLER import HANDLER
from HOST import HOST
from ITEM import ITEM
from MSG import MSG
from SESSION import SESSION
from STRUCT import STRUCT

class VAULT(HOST, HANDLER):
    ''' 🗄️ https://quip.com/IZapAfPZPnOD '''
    

    def __init__(self):    
        self.On('VerifyDownload@Host', self._verifyWalletSignature)
        self.On('VerifyUpload@Host', self._verifyWalletSignature)
        

    
    def _verifyWalletSignature(self, msg:MSG, session:ITEM):
        # 🏃 If the user is bound, check the signature with the public in the vault.
        if not session.IsMissingOrEmpty('Wallet.WalletID'):
            walletInSession = session.Att('Wallet')
            publicKey = self.Wallets().Get(walletInSession).Require('PublicKey')
            msg.VerifySignature(publicKey)

    
    # ✅ DONE
    def Binds(self):
        ''' 🪣 https://quip.com/IZapAfPZPnOD#temp:C:PDZ669f275089004e74b3004d236 
        {
            "Broker": "any-broker.com",
            "BindID": "793af21d-12b1-4cea-8b55-623a19a28fc5",
            "PublicKey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDH+wPrKYG1KVlzQUVtBghR8n9dzcShSZo0+3KgyVdOea7Ei7vQ1U4wRn1zlI5rSqHDzFitblmqnB2anzVvdQxLQ3UqEBKBfMihnLgCSW8Xf7MCH+DSGHNvBg2xSNhcfEmnbLPLnbuz4ySn1UB0lH2eqxy50zstxhTY0binD9Y+rwIDAQAB",
            "Code": "iata.org/SSR/WCHR",
            "Confirmed": True
        }
        '''
        return self.DYNAMO('BINDS', keys=['Broker', 'BindID'])
    

    # ✅ DONE
    def GetBind(self, broker:str, bindID:str) -> ITEM:
        item = self.Binds().Get({
            'Broker': broker, 
            'BindID': bindID
        })
        return ITEM(item)
    

    # ✅ DONE
    def InvokeBound(self, source:str, vault:str, sessionID:str, binds:List[any], publicKey:str):
        ''' 🏃 Broker.Bound: 🐌 https://quip.com/oSzpA7HRICjq/-Broker-Binds#temp:C:DSD3f7309f961e24f0ebb5897e2f '''        

        self.MESSENGER().Push(
            source= source,
            to= vault,
            body= {
                "SessionID": sessionID,
                "PublicKey": publicKey,
                "Binds": binds
            })

    
    def HandleBound(self, event):
        ''' 
        🗄️🐌 https://quip.com/oSzpA7HRICjq/-Broker-Binds#temp:C:DSD3f7309f961e24f0ebb5897e2f 
        🗄️🐌 https://quip.com/IZapAfPZPnOD#temp:C:PDZf81764583b31439f999550159  
        "Body": {
            "SessionID": "...",
            "PublicKey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDH+wPrKYG1KVlzQUVtBghR8n9dzcShSZo0+3KgyVdOea7Ei7vQ1U4wRn1zlI5rSqHDzFitblmqnB2anzVvdQxLQ3UqEBKBfMihnLgCSW8Xf7MCH+DSGHNvBg2xSNhcfEmnbLPLnbuz4ySn1UB0lH2eqxy50zstxhTY0binD9Y+rwIDAQAB",
            "Binds": [{
                "ID": "793af21d-12b1-4cea-8b55-623a19a28fc5",
                "Code": "iata.org/SSR/WCHR"
            }]
        }
        '''
        msg, session = self.VerifySession(event)
                
        # Optionally, confirm the binding with an 😶 Identity
        outcomes = { 
            'Confirmed': True,
            'VaultID': None
        }
        self.Trigger('HandleBind@Vault', event, outcomes)

        vaultID = outcomes['VaultID']

        # Update 🪣 Session
        session.Att('VaultID', vaultID)
        session.Update()

        # Add to 🪣 Binds
        binds = []
        for code in msg.Structs('Codes'):

            bindID = self.UUID()
            binds.append({
                "BindID": bindID,
                "Code": code
            })

            # TODO: consider removing this table.
            self.Binds().Upsert({
                "BindID": bindID,
                "Broker": broker,
                "WalletID": walletID,
                "Code": code.Require('Code')
            })

        # Add to 🪣 Wallets 
        wallet = self.Wallets().Upsert({
            'Broker': broker,
            'WalletID': walletID,
            'VaultID': vaultID,
            'Confirmed': outcomes['Confirmed'],
            'PublicKey': msg.Require('PublicKey'),
        })

        old = wallet.Att('Binds', default=[])
        wallet.Att('Binds', old + binds)
        wallet.Update()

        # Call 🐌 Bound: 🤵📎 Broker. Binds
        self.BROKER().InvokeBound(
            source='Vault-Bind',
            to= broker,
            walletID= walletID,
            binds= binds,
            request= event)


    # ✅ DONE
    def Disclosures(self):
        ''' 🪣 https://quip.com/IZapAfPZPnOD#temp:C:PDZ71e7244be24842df9b773d541 
        {
            "Consumer": "any-host.com",
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",   
            "Timestamp": "2018-12-10T13:45:00.000Z",
            "Binds": [
                "BindID": "793af21d-12b1-4cea-8b55-623a19a28fc5",
                "Status": "@OTP",
                "Continue": "6704488d-fb53-446d-a52c-a567dac20d20"
            ]
        }'''
        return self.DYNAMO('DISCLOSURES', keys=['DisclosureID'])
    

    # ✅ DONE
    def TrustsConsumer(self, domain, code) -> bool:
        return self.GRAPH().InvokeTrusted(
            domain= domain,
            context= 'CONSUMER',
            code= code
        )


    def HandleContinue(self, event):
        ''' 📦🐌 https://quip.com/IZapAfPZPnOD#temp:C:PDZ67394972376e4fb8979d41209 '''
        '''
        "Body": {
            "Continue": "6704488d-fb53-446d-a52c-a567dac20d20"
        }
        '''
        msg = self.MSG(event)


    def HandleDisclose(self, event):
        ''' 🧑‍🦰🐌 https://quip.com/IZapAfPZPnOD#temp:C:PDZa3f3ba7f94154a2fbd520e931 
        "Body": {
            "Consumer": "any-coffee-shop.com",
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",
            "Language": "en-us",
            "Binds": [{
                "BindID": "793af21d-12b1-4cea-8b55-623a19a28fc5"
            }],
        }
        '''
        msg = self.MSG(event)

        # Validate the user’s signature in the ✉️ Msg
        # -> compare with the key in 🪣 Wallets

        session = self.Sessions(event)

        wallet = self.Wallet(
            broker= session.Broker(),
            walletID= session.WalletID()
        )
        wallet.ValidateSignature(msg)
                
        # Verify if 🔎 Consumer is trustable:
        # -> call 🚀 Trusted: 🕸 Graph (CONSUMER)

        for item in msg.Structs('Binds'):
            bindID = item.Require('BindID')
            bind = self.Bind(bindID)

            if not self.TrustsConsumer(
                domain= msg.Require('Session.Consumer'),
                code= bind.Code()
            ): 
                raise Exception(f'Consumer not trusted for {bind.Code()}')
            
            # Ask any additional question to the user (e.g., OTP):
            # -> Add to 🪣 Disclosures
            # -> Call 🐌 Prompt: 🤵📎 Broker. Prompt

            # Send details to 🔎 Consumer:
            # -> 🐌 Consume: 🔎 Consumer


    # ✅ DONE
    def InvokeSuppress(self, to:str, consumer:str, sessionID:str, source:str):
        ''' 🤵🏃 https://quip.com/IZapAfPZPnOD#temp:C:PDZeda25d5a05a3470a994e6689d '''
        self.MESSENGER().Push(
            to= to,
            subject= 'Suppress@Vault',
            source= source,
            body= {
                "Consumer": consumer,
                "SessionID": sessionID
            }
        )


    # ✅ DONE
    def HandleSuppress(self, event):
        ''' 🤵🐌 https://quip.com/IZapAfPZPnOD#temp:C:PDZeda25d5a05a3470a994e6689d 
        "Body": {
            "Consumer": "airfrance.fr",
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa4"
        }
        '''
        msg = self.MSG(event)
        
        # If the session is tracked, stop it - e.g.: 
        #   GIVEN a vault that is a palm reader 
        #     AND the palm reader is actively looking for the session’s user
        #    WHEN suppressed 
        #    THEN stop searching for it, and stop sending findings to the host.
        self.Trigger('HandleSupress@Vault', event)
        
        # Remove the session from 🪣 Disclosures
        # If the session is not found on disclosures, just discard the message.
        disclosure = self.Disclosures().Get(msg)
        if not disclosure.IsMissingOrEmpty():
            disclosure.Delete()


    # ✅ DONE
    def InvokeUnbind(self, source:str, vault:str, bindID: str):
        self.MESSENGER().Push(
            to= vault,
            subject= 'Unbind@Vault',
            source= source,
            body= {
                "BindID": bindID
            }
        )



    def HandleUnbind(self, event):
        ''' 🤵🐌 https://quip.com/IZapAfPZPnOD#temp:C:PDZ7c06cfb34057465cadb320937 
        "Body": {
            "BindID": "793af21d-12b1-4cea-8b55-623a19a28fc5"
        }
        '''
        msg = self.MSG(event)
        bind = self.Binds().Get(msg)
        bind.Require()
        bind.Match('Broker', msg.From())
        bind.Delete()