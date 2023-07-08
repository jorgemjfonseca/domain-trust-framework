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
        

    # ✅ DONE
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
        return self.DYNAMO('WALLETS', keys=['Broker', 'WalletID'])
    

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
        return self.DYNAMO('BINDS', keys=['BindID'])
    

    # ✅ DONE
    def Disclosures(self):
        ''' 🪣 https://quip.com/IZapAfPZPnOD#temp:C:PDZ71e7244be24842df9b773d541 '''
        return self.DYNAMO('DISCLOSURES', keys=['DisclosureID'])
    

    # ✅ DONE
    def TrustsConsumer(self, domain, code) -> bool:
        return self.GRAPH().InvokeTrusted(
            domain= domain,
            context= 'CONSUMER',
            code= code
        )


    # ✅ DONE
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
        msg, session = self.VerifyWalletMsg(event)
        
        # Optionally, confirm the binding with an 😶 Identity
        outcomes = { 
            'Confirmed': True,
            'VaultID': None
        }
        self.Trigger('HandleBind@Vault', event, outcomes)

        broker = session.Require('Wallet.Broker')
        walletID = msg.Require('WalletID')
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


    def HandleContinue(self, event):
        ''' 🐌 https://quip.com/IZapAfPZPnOD#temp:C:PDZ67394972376e4fb8979d41209 '''
        '''
        "Body": {
            "Continue": "6704488d-fb53-446d-a52c-a567dac20d20"
        }
        '''
        msg = self.MSG(event)


    def HandleDisclose(self, event):
        ''' 🐌 https://quip.com/IZapAfPZPnOD#temp:C:PDZa3f3ba7f94154a2fbd520e931 '''
        '''
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



    def HandleSuppress(self, event):
        ''' 🐌 https://quip.com/IZapAfPZPnOD#temp:C:PDZeda25d5a05a3470a994e6689d '''
        '''
        "Body": {
            "Consumer": "airfrance.fr",
                "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa4"
        }
        '''
        msg = self.MSG(event)


    def HandleUnbind(self, event):
        ''' 🐌 https://quip.com/IZapAfPZPnOD#temp:C:PDZ7c06cfb34057465cadb320937 '''
        '''
        "Body": {
            "BindID": "793af21d-12b1-4cea-8b55-623a19a28fc5"
        }
        '''
        msg = self.MSG(event)