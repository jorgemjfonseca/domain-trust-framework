# 📚 NOTIFIER

from DTFW import DTFW
from MSG import MSG
from STRUCT import STRUCT
dtfw = DTFW()


class NOTIFIER:
    ''' 📣 https://quip.com/PCunAKUqSObO/-Notifier '''
    

    # ✅ DONE
    def Invoke(self, notifier:str, data: any, source:str):
        ''' 👉 ends a message to the notifier of the wallet. '''
        msg = dtfw.WRAP(to=notifier, body=data)
        dtfw.MESSENGER().Send(msg=msg, source=source)


    def HandleOnboard(self, event):
        ''' 🚀 https://quip.com/PCunAKUqSObO#temp:C:UKEb7e4672f7c6a4fcdb1fbbd882 '''
        '''
        "Body": {
            "Language": "en-us",
            "PublicKey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDH+wPrKYG1KVlzQUVtBghR8n9dzcShSZo0+3KgyVdOea7Ei7vQ1U4wRn1zlI5rSqHDzFitblmqnB2anzVvdQxLQ3UqEBKBfMihnLgCSW8Xf7MCH+DSGHNvBg2xSNhcfEmnbLPLnbuz4ySn1UB0lH2eqxy50zstxhTY0binD9Y+rwIDAQAB"
        }
        '''    
        msg = dtfw.MSG(event)


    def HandleTranslated(self, event):
        ''' 🐌 https://quip.com/PCunAKUqSObO#temp:C:UKE27bcb1e6dd3e493f88b36b695 '''
        '''
        "Body": {
            "WalletID": "1313c5c6-4038-44ea-815b-73d244eda85e",
            "Language": "pt-br"
        }
        '''    
        msg = dtfw.MSG(event)
        

    def HandleUpdated(self, event):
        ''' 🐌 https://quip.com/PCunAKUqSObO#temp:C:UKE46862f6d9130436a9c9396213 '''
        '''
        "Body": {
            "WalletID": "1313c5c6-4038-44ea-815b-73d244eda85e",
            "Updates": ["CREDENTIALS"]
        }
        '''    
        msg = dtfw.MSG(event)
        

    def HandlePrompt(self, event):
        ''' 🐌 https://quip.com/PCunAKUqSObO#temp:C:UKEc385117d31e042358eaa48ea1 '''
        '''
        "Body": {
            "WalletID": "1313c5c6-4038-44ea-815b-73d244eda85e",
            "Context": {...},
            "Prompt": {...}
        }
        '''    
        msg = dtfw.MSG(event)
        

    def HandleBindable(self, event):
        ''' 🐌 https://quip.com/PCunAKUqSObO#temp:C:UKEe59fd4b4d73345348afd67d5f '''
        '''
        "Body": {
            "WalletID": "1313c5c6-4038-44ea-815b-73d244eda85e",
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",
            "Codes": [
                {
                    "Code": "iata.org/SSR/WCHR",
                    "Translation": "Wheelchair assistance required; passenger can walk short distance up or down stairs."
                }
            ]
        }
        '''    
        msg = dtfw.MSG(event)
        

    def HandleBound(self, event):
        ''' 🐌 https://quip.com/PCunAKUqSObO#temp:C:UKE1c11313f9113455b9857c5bc2 '''
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
        msg = dtfw.MSG(event)
        

    def HandleIssued(self, event):
        ''' 🐌 https://quip.com/PCunAKUqSObO#temp:C:UKE43477024fb334f3c9bb85c34e '''
        '''
        "Body": {
            "WalletID": "1313c5c6-4038-44ea-815b-73d244eda85e",
            "CredentialID": "7bcf138b-db79-4a42-9d36-2655f8ff1f7c",
            "Code": "iata.org/SSR/WCHR",
            "Translation": "Wheelchair for ramp",
            "Source": "https://example.com/tf/credentials/7bcf138b-db79-4a42-9d36-2655f8ff1f7c"
        }
        '''    
        msg = dtfw.MSG(event)
        

    def HandleRevoked(self, event):
        ''' 🐌 https://quip.com/PCunAKUqSObO#temp:C:UKE140ed710db89444c956ea2eac '''
        '''
        "Body": {
            "WalletID": "1313c5c6-4038-44ea-815b-73d244eda85e",
            "CredentialID": "7bcf138b-db79-4a42-9d36-2655f8ff1f7c",
            "Source": "https://example.com/tf/credentials/7bcf138b-db79-4a42-9d36-2655f8ff1f7c"
        }
        '''    
        msg = dtfw.MSG(event)
        

    def HandleQuery(self, event):
        ''' 🐌 https://quip.com/PCunAKUqSObO#temp:C:UKE78fd4570e5dc440f979d5dd07 '''
        '''
        "Body": {
            "WalletID": "1313c5c6-4038-44ea-815b-73d244eda85e",
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",
            "Translation": "Example Airlines"
            "Bound": [{
                "Code": "iata.org/SSR/WCHR",
                "Translation": "Wheelchair assistance required"
                "Vaults": [{
                    "Vault": "ec.europa.eu",
                    "Translation": "European Union"
                }]
            }],
            "Unbound": [{
                "Code": "iata.org/SSR/AOXY",
                "Translation": "Airline Supplied Oxygen"
                "Vaults": [{
                    "Vault": "ec.europa.eu",
                    "Translation": "European Union"
                }]
            }]
        }
        '''    
        msg = dtfw.MSG(event)
        

    def HandleCharge(self, event):
        ''' 🐌 https://quip.com/PCunAKUqSObO#temp:C:UKE3093906b2c254c68b94bfc7ad '''
        '''
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "Request": {...},
            "Options": [
                {
                    "Payer": "pay.google.com",
                    "Translation": "Google Wallet",
                    "Collector": "revolut.com"
                }, 
                {
                    "Payer": "paypal.com",
                    "Translation": "PayPal",
                    "Collector": "paypal.com"
                }
            ]
        }
        '''    
        msg = dtfw.MSG(event)