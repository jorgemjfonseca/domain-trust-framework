
# 📚 BROKER_SETUP

def test():
    return 'this is BROKER_SETUP test.'

from DYNAMO import DYNAMO
from ITEM import ITEM
from MSG import MSG
from DTFW import DTFW

dtfw = DTFW()


class BROKER_SETUP:
    ''' 👉 https://quip.com/zaYoA4kibXAP/-Broker-Setup '''

    
    def HandleOnboard(self, event):
        ''' 👉 https://quip.com/zaYoA4kibXAP#temp:C:DQN1f2d80d98fdd4e69a98a32887 '''
        '''
        "Body": {
            "Language": "en-us",
            "PublicKey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDH+wPrKYG1KVlzQUVtBghR8n9dzcShSZo0+3KgyVdOea7Ei7vQ1U4wRn1zlI5rSqHDzFitblmqnB2anzVvdQxLQ3UqEBKBfMihnLgCSW8Xf7MCH+DSGHNvBg2xSNhcfEmnbLPLnbuz4ySn1UB0lH2eqxy50zstxhTY0binD9Y+rwIDAQAB"
        }
        '''
        dtfw.Msg(event)

    
    def HandleTranslate(self, event):
        ''' 👉 https://quip.com/zaYoA4kibXAP#temp:C:DQN0cc419509625497ea39fa08e9 '''
        '''
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "Language": "en-us"
        }
        '''
        dtfw.Msg(event)

    
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

    
    