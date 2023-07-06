
# 📚 BROKER_SETUP

import string
import random

from DTFW import DTFW
dtfw = DTFW()


class BROKER_SETUP:
    ''' 👉 https://quip.com/zaYoA4kibXAP/-Broker-Setup '''


    def Wallets(): 
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
            }]
        }
        '''
        return dtfw.Dynamo('WALLETS', keys=['WalletID'])

    
    
    def Locator(size=6, chars=string.ascii_uppercase + string.digits):
        ''' 👉 https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits '''
        return ''.join(random.choice(chars) for _ in range(size))
    

    def HandleOnboard(self, event):
        ''' 👉 https://quip.com/zaYoA4kibXAP#temp:C:DQN1f2d80d98fdd4e69a98a32887 '''
        '''
        "Body": {
            "Language": "en-us",
            "PublicKey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDH+wPrKYG1KVlzQUVtBghR8n9dzcShSZo0+3KgyVdOea7Ei7vQ1U4wRn1zlI5rSqHDzFitblmqnB2anzVvdQxLQ3UqEBKBfMihnLgCSW8Xf7MCH+DSGHNvBg2xSNhcfEmnbLPLnbuz4ySn1UB0lH2eqxy50zstxhTY0binD9Y+rwIDAQAB"
        }
        '''
        msg = dtfw.Msg(event) 

        brokerDomain = '<TBD>'
        brokerLocator = self.Locator()

        item = {
            'WalletID': dtfw.Utils().UUID(),
            'Locator': brokerLocator,
            'WalletQR': f'🤝dtfw.org/WALLET,1,{brokerDomain},{brokerLocator}',
            'WalletQRURL': f'https://dtfw.any-broker.com/qr/1AB2CD',
            'Language': msg.Require('Language'),
            'PublicKey': msg.Require('PublicKey'),
            'Notifier': msg.From(),
            'Hosts': []
        }
        
        self.Wallets().Merge(item)

        return {
            "WalletID": item.Require('WalletID'),
            "Locator": item.Require('Locator')
        }

    
    def HandleTranslate(self, event):
        ''' 👉 https://quip.com/zaYoA4kibXAP#temp:C:DQN0cc419509625497ea39fa08e9 '''
        '''
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "Language": "en-us"
        }
        '''
        msg = dtfw.Msg(event)
        wallet = dtfw.Broker().Setup().Wallets().Get(msg)
        wallet.Require()

        dtfw.Broker().Sessions().Translate(msg)
        dtfw.Broker().Binds().Translate(msg)
        dtfw.Broker().Credentials().Translate(msg)
        
        out = {
            "WalletID": msg.Require('WalletID'),
            "Language": msg.Require('Language')
        }

        dtfw.Notifier()



    
    def HandleReplace(self, event):
        ''' 👉 https://quip.com/zaYoA4kibXAP#temp:C:DQN148380274b884fc7b9d104743 '''
        '''
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a"
        }
        '''
        dtfw.Msg(event)

    
    def HandleQR(self, event):
        ''' 👉 https://quip.com/zaYoA4kibXAP#temp:C:DQN7a84fa77334c4b00b0173b9c8 '''
        '''
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a"
        }
        '''
        dtfw.Msg(event)

    
    