# 📚 VAULT

def test():
    return 'this is VAULT test.'


from HOST import HOST
from ITEM import ITEM
from MSG import MSG

class VAULT(HOST):
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
    def Wallets(self):
        ''' 🪣 https://quip.com/IZapAfPZPnOD#temp:C:PDZ4a9cd6bab1ef4d08a9b4627f0 
        {   
            "VaultID": "EX123456",
            "Broker": "any-broker.com",
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "PublicKey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDH+wPrKYG1KVlzQUVtBghR8n9dzcShSZo0+3KgyVdOea7Ei7vQ1U4wRn1zlI5rSqHDzFitblmqnB2anzVvdQxLQ3UqEBKBfMihnLgCSW8Xf7MCH+DSGHNvBg2xSNhcfEmnbLPLnbuz4ySn1UB0lH2eqxy50zstxhTY0binD9Y+rwIDAQAB",
            "Confirmed": True
        }'''
        return self.Dynamo('WALLETS', keys=['Broker', 'WalletID'])
    

    # ✅ DONE
    def Binds(self):
        ''' 🪣 https://quip.com/IZapAfPZPnOD#temp:C:PDZ669f275089004e74b3004d236 
        {
            "BindID": "793af21d-12b1-4cea-8b55-623a19a28fc5",
            "Broker": "any-broker.com",
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "Code": "iata.org/SSR/WCHR"
        }
        '''
        return self.Dynamo('BINDS', keys=['BindID'])
    

    # ✅ DONE
    def Disclosures(self):
        ''' 🪣 https://quip.com/IZapAfPZPnOD#temp:C:PDZ71e7244be24842df9b773d541 '''
        return self.Dynamo('DISCLOSURES', keys=['DisclosureID'])
    

    # ✅ DONE
    def TrustsConsumer(self, domain, code) -> bool:
        return self.Graph().InvokeTrusted(
            domain= domain,
            context= 'CONSUMER',
            code= code
        )


    def HandleBind(self, event):
        ''' 🐌 https://quip.com/IZapAfPZPnOD#temp:C:PDZf81764583b31439f999550159 '''
        '''
        "Body": {
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "PublicKey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDH+wPrKYG1KVlzQUVtBghR8n9dzcShSZo0+3KgyVdOea7Ei7vQ1U4wRn1zlI5rSqHDzFitblmqnB2anzVvdQxLQ3UqEBKBfMihnLgCSW8Xf7MCH+DSGHNvBg2xSNhcfEmnbLPLnbuz4ySn1UB0lH2eqxy50zstxhTY0binD9Y+rwIDAQAB",
            "Codes": [{
                    "Code": "iata.org/SSR/WCHR"
            }]
        }
        '''
        msg = self.Msg(event)

        # Validate if the session is still active in 🪣 Sessions: 🤗 Host
        session = self.Host().ValidateSession(msg)
        
        # Optionally, confirm the binding with an 😶 Identity
        self.Trigger('VALIDATE@BIND', msg)

        # Add to 🪣 Wallets 
        vaultID = "<TBC>"
        broker = session.Require('Wallet.Broker')
        walletID = msg.Require('WalletID')

        self.Wallets().Upsert(
            id= self.WalletKey(
                broker= broker,
                walletID= walletID
            ),
            item= {
                "VaultID": vaultID,
                "Broker": broker,
                "WalletID": walletID,
                "PublicKey": msg.Require('PublicKey'),
                "Confirmed": False
            }
        )

        self.Sessions().Upsert(
            id= session.Require['SessionID'], 
            item= { "VaultID": vaultID }
        )

        # Add to 🪣 Binds
        binds = []

        for code in msg.Structs('Codes'):

            bindID = dtfw.Utils().UUID()

            binds.append({
                "BindID": bindID,
                "Code": code
            })

            self.Binds().Upsert(
                id= bindID,
                item= {
                    "BindID": bindID,
                    "Broker": broker,
                    "WalletID": walletID,
                    "Code": code.Require('Code')
                }
            )

        # Call 🐌 Bound: 🤵📎 Broker. Binds
        bound = dtfw.Msg()
        bound.To(msg.From())
        bound.Body({
            "WalletID": msg.Require('WalletID'),
            "Request": event,
            "Binds": binds
        })

        dtfw.Messenger().Send(bound, source='Vault-Bind')
        
        ''' Broker.Bound: 🐌 https://quip.com/oSzpA7HRICjq/-Broker-Binds#temp:C:DSD3f7309f961e24f0ebb5897e2f '''
        '''
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "Request": {...}
            "Binds": [{
                "BindID": "793af21d-12b1-4cea-8b55-623a19a28fc5",
                "Code": "iata.org/SSR/WCHR"
            }]
        }
        '''        


    def HandleContinue(self, event):
        ''' 🐌 https://quip.com/IZapAfPZPnOD#temp:C:PDZ67394972376e4fb8979d41209 '''
        '''
        "Body": {
            "Continue": "6704488d-fb53-446d-a52c-a567dac20d20"
        }
        '''
        msg = dtfw.Msg(event)


    def HandleDisclose(self, event):
        ''' 🐌 https://quip.com/IZapAfPZPnOD#temp:C:PDZa3f3ba7f94154a2fbd520e931 '''
        '''
        "Body": {
            "Binds": [{
                "BindID": "793af21d-12b1-4cea-8b55-623a19a28fc5"
            }],
            "Session": {
                "Consumer": "any-coffee-shop.com",
                "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",
                "Language": "en-us"
            }
        }
        '''
        msg = dtfw.Msg(event)

        # Validate the user’s signature in the ✉️ Msg
        # -> compare with the key in 🪣 Wallets

        sessionID = msg.Require('Session.SessionID')
        session = dtfw.Host().Session(sessionID)

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



    def HandleSuppress(self, event):
        ''' 🐌 https://quip.com/IZapAfPZPnOD#temp:C:PDZeda25d5a05a3470a994e6689d '''
        '''
        "Body": {
            "Consumer": "airfrance.fr",
                "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa4"
        }
        '''
        msg = dtfw.Msg(event)


    def HandleUnbind(self, event):
        ''' 🐌 https://quip.com/IZapAfPZPnOD#temp:C:PDZ7c06cfb34057465cadb320937 '''
        '''
        "Body": {
            "BindID": "793af21d-12b1-4cea-8b55-623a19a28fc5"
        }
        '''
        msg = dtfw.Msg(event)