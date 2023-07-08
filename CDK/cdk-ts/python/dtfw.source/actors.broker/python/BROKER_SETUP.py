
# 📚 BROKER_SETUP

import string
import random
from BROKER import BROKER

from DTFW import DTFW


# ✅ DONE
class BROKER_SETUP():
    ''' 👉 https://quip.com/zaYoA4kibXAP/-Broker-Setup '''


    # ✅ DONE
    def Wallets(self): 
        ''' 👉 https://quip.com/zaYoA4kibXAP#temp:C:DQN5a1b1a16ec7f4a29907cd1215'''
        '''
        {    
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "WalletQR": "🤝dtfw.org/WALLET,1,any-trust-broker.com,1AB2CD",
            "WalletQRURL": "https://any.broker.com/tf/qr/1AB2CD",
            "Language": "en-us",
            "Locator": "1AB2CD",
            "PublicKey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDH+wPrKYG1KVlzQUVtBghR8n9dzcShSZo0+3KgyVdOea7Ei7vQ1U4wRn1zlI5rSqHDzFitblmqnB2anzVvdQxLQ3UqEBKBfMihnLgCSW8Xf7MCH+DSGHNvBg2xSNhcfEmnbLPLnbuz4ySn1UB0lH2eqxy50zstxhTY0binD9Y+rwIDAQAB",
            "Notifier": "any-wallet.com",
            "Hosts": [{
                "Host": "iata.org",
                "Translation": "IATA",
                "Language": "en-us",
                "Sessions": [{
                    "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",
                    "SessionTime": "2018-12-10T13:45:00.000Z"
                }]
            }],
            "Vaults": [{
                "Vault": "iata.org",
                "Translation": "IATA",
                "Binds": [{
                    "BindID": "793af21d-12b1-4cea-8b55-623a19a28fc5",
                    "Code": "iata.org/SSR/WCHR",
                    "Translation": "Wheelchair for ramp"
                }]
            }],
            "Issuers": {
                "Issuer": "nhs.uk",
                "Translation": "NHS",
                "Credentials": [{
                    "CredentialID": "7bcf138b-db79-4a42-9d36-2655f8ff1f7c",
                    "Code": "iata.org/SSR/WCHR",
                    "Translation": "Wheelchair for ramp"
                    "Path": "/storage/tf/creds/nhs.uk/7bcf138b-db79-4a42-9d36-2655f8ff1f7c"
                }]
            }
        }
        '''
        return self.Dynamo('WALLETS', keys=['WalletID'])


    # ✅ DONE
    def Locators(self):
        ''' 👉 https://quip.com/zaYoA4kibXAP#temp:C:DQN0b6b0f28ad7b4ec8b5cac187e '''
        '''
        {    
            "Locator": "1AB2CD",
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a"
        }
        '''
        return self.Dynamo('LOCATORS', keys=['Locator'])
    

    # ✅ DONE
    def Locator(self, size=6, chars=string.ascii_uppercase + string.digits):
        ''' 👉 https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits '''
        return ''.join(random.choice(chars) for _ in range(size))
    

    # ✅ DONE
    def UnusedLocator(self):
        ''' 👉 Look for an unused locator. '''
        repeat = True
        brokerLocator = None
        while repeat:
            brokerLocator = self.Locator()
            existing = self.Locators().Get(brokerLocator)
            if existing.IsMissingOrEmpty():
                repeat = False
        return brokerLocator
    

    # ✅ DONE
    def Domain(self) -> str:
        return self.Utils().Enrironment('DOMAIN')


    # ✅ DONE
    def VerifySignature(self, event):
        msg = self.Msg(event)
        wallet = self.Wallets().Get(msg.Body())
        publicKey = wallet.Require('PublicKey')
        msg.VerifySignature(publicKey)
        return msg, wallet


    # ✅ DONE
    def HandleOnboard(self, event):
        ''' 🚀 https://quip.com/zaYoA4kibXAP#temp:C:DQN1f2d80d98fdd4e69a98a32887 '''
        '''
        "Body": {
            "Language": "en-us",
            "PublicKey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDH+wPrKYG1KVlzQUVtBghR8n9dzcShSZo0+3KgyVdOea7Ei7vQ1U4wRn1zlI5rSqHDzFitblmqnB2anzVvdQxLQ3UqEBKBfMihnLgCSW8Xf7MCH+DSGHNvBg2xSNhcfEmnbLPLnbuz4ySn1UB0lH2eqxy50zstxhTY0binD9Y+rwIDAQAB"
        }
        '''
        msg = self.Msg(event) 

        walletID = self.UUID()
        brokerDomain = self.Domain()
        brokerLocator = self.UnusedLocator()
        
        # Configure the locator.
        locator = {
            'Locator': brokerLocator,
            'WalletID': walletID
        }

        # Configure the wallet.
        wallet = {
            'WalletID': walletID,
            'Locator': brokerLocator,
            'WalletQR': f'🤝dtfw.org/WALLET,1,{brokerDomain},{brokerLocator}',
            'WalletQRURL': f'https://{brokerDomain}/qr/{brokerLocator}',
            'Language': msg.Require('Language'),
            'PublicKey': msg.Require('PublicKey'),
            'Notifier': msg.From(),
            'Hosts': []
        }
        
        # Save both to DB.
        # TODO: make it a transaction, or a chained event.
        self.Locators().Insert(locator)
        self.Wallets().Insert(wallet)

        return {
            "WalletID": wallet.Require('WalletID'),
            "Locator": wallet.Require('Locator')
        }

    
    # ✅ DONE
    def HandleTranslate(self, event):
        ''' 🐌 https://quip.com/zaYoA4kibXAP#temp:C:DQN0cc419509625497ea39fa08e9 '''
        '''
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "Language": "en-us"
        }
        '''
        msg, wallet = self.VerifySignature(event)

        # Call 🚀 Translate: 🕸 Graph for:
        domains = []
        for host in wallet.Structs('Hosts'):
            domains.append(host.Require('Host'))
        for vault in wallet.Structs('Vaults'):
            domains.append(vault.Require('Vault'))
        for issuer in wallet.Structs('Issuers'):
            domains.append(issuer.Require('Issuer'))

        ret = self.Graph().InvokeTranslate({
            "Language": msg.Require('Language'),
            "Domains": domains
        })
        '''
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

        for lang in ret.Structs('Domains'):
            for host in wallet.Structs('Hosts'):
                if host.Att('Host') == lang.Att('Domain'):
                    host.Att('Translation', lang.Require('Translation'))
            for vault in wallet.Structs('Vaults'):
                if vault.Att('Vault') == lang.Att('Domain'):
                    vault.Att('Translation', lang.Require('Translation'))
            for issuer in wallet.Structs('Issuers'):
                if issuer.Att('Issuer') == lang.Att('Domain'):
                    issuer.Att('Translation', lang.Require('Translation'))

        # Save to DB
        wallet.Update()

        # Call 🐌 Translated: 📣 Notifier
        self.Notifier().Invoke(
            notifier= wallet.Require('Notifier'),
            data= {
                "WalletID": msg.Require('WalletID'),
                "Language": msg.Require('Language')
            },
            source= 'Broker-Translate'
        )

    
    # ✅ DONE
    def HandleReplace(self, event):
        ''' 🚀 https://quip.com/zaYoA4kibXAP#temp:C:DQN148380274b884fc7b9d104743 '''
        '''
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a"
        }
        '''
        msg = self.Msg(event)

        wallet = self.Wallets().Get(msg)
        wallet.Require()

        # Delete the old locator.
        self.Locators().Get(wallet).Delete()
        
        # Configure the new locator.
        brokerLocator = self.UnusedLocator()
        self.Locators().Insert({
            'Locator': brokerLocator,
            'WalletID': wallet.Require('WalletID')
        })

        # Update the wallet.
        wallet.Att('Locator', brokerLocator)
        wallet.Update()

        '''
        {
            "Locator": "2AB2CD"
        }
        '''
        return {
            "Locator": brokerLocator
        }

    
    # ✅ DONE
    def HandleQR(self, event):
        ''' 🚀 https://quip.com/zaYoA4kibXAP#temp:C:DQN7a84fa77334c4b00b0173b9c8 '''
        '''
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a"
        }
        '''
        msg = self.Msg(event)
        wallet = self.Wallets().Get(msg)
        wallet.Require()

        brokerDomain = self.Domain()
        locator = wallet.Require('Locator')
        data = f'🤝dtfw.org/WALLET,1,{brokerDomain},{locator}'

        return {
            "Base64": self.GetImageQR(data)
        }

        

    
    