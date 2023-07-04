# 📚 VAULT

def test():
    return 'this is VAULT test.'

from DYNAMO import DYNAMO
from ITEM import ITEM
from MSG import MSG
from DTFW import DTFW

dtfw = DTFW()



class VAULT:
    

    def wallets(self) -> DYNAMO:
        return dtfw.Dynamo('WALLETS')
    def walletKey(self, broker, walletID):
        return f'{broker}/{walletID}'
    def Wallet(self, broker, walletID) -> ITEM:
        key = self.walletKey(broker, walletID)
        return self.wallets().Item(key)
    

    def binds(self) -> DYNAMO:
        return dtfw.Dynamo('BINDS')
    def bind(self, bindID) -> ITEM:
        return self.binds().Item(bindID)
    

    def disclosures(self) -> DYNAMO:
        return dtfw.Dynamo('DISCLOSURES')
    def disclosure(self, disclosureID) -> ITEM:
        return self.disclosures().Item(disclosureID)
    

    def grants(self) -> DYNAMO:
        return dtfw.Dynamo('GRANTS')
    def grantKey(self, broker, walletID):
        return f'{broker}/{walletID}'
    def grant(self, broker, walletID) -> ITEM:
        key = self.grantKey(broker, walletID)
        return self.grants().Item(key)


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
        msg = dtfw.Msg(event)

        # Validate if the session is still active in 🪣 Sessions: 🤗 Host
        session = dtfw.Host().ValidateSession(msg)
        
        # Optionally, confirm the binding with an 😶 Identity

        # Add to 🪣 Wallets 
        vaultID = "<TBC>"
        broker = session.Require('Wallet.Broker')
        walletID = msg.Require('WalletID')

        self.wallets().Merge(
            id= self.walletKey(
                broker= broker,
                walletID= walletID
            ),
            item= {
                "VaultID": vaultID,
                "Broker": broker,
                "WalletID": walletID,
                "PublicKey": msg.Require('PublicKey'),
                "Confirmed": True
            }
        )

        dtfw.Host().Sessions().Merge(
            id= session.Require['SessionID'], 
            item= { "VaultID": vaultID }
        )

        # Add to 🪣 Binds
        binds = []

        for code in msg.Items('Codes'):

            bindID = dtfw.Utils().UUID()

            binds.append({
                "BindID": bindID,
                "Code": code
            })

            self.binds().Merge(
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
                "Consumer": "starbucks.com",
                "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",
                "Language": "en-us"
            }
        }
        '''
        msg = dtfw.Msg(event)
        sessionID = msg.Require('Session.SessionID')
        session = dtfw.Host().Session(sessionID)
        wallet = self.Wallet(
            broker= session.Broker(),
            walletID= session.WalletID()
        )
        
        dtfw.SyncApi().Dkim().ValidateSignature()
        wallet.Match('PublicKey', msg.Signature())
        msg.Signature()
        

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