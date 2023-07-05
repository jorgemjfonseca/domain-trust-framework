
# 📚 BROKER_SESSIONS

def test():
    return 'this is BROKER_SESSIONS test.'

from DYNAMO import DYNAMO
from ITEM import ITEM
from MSG import MSG
from DTFW import DTFW

dtfw = DTFW()


class BROKER_SESSIONS:
    ''' 👉 https://quip.com/HrgkAuQCqBez#bXDABAe5brB '''

    
    def HandleSessions(self, event):
        ''' 👉 https://quip.com/HrgkAuQCqBez#temp:C:bXD09ae7595fe4943d5985d83fd0 '''
        '''
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a"
        }
        '''
        dtfw.Msg(event)


    def HandleTalker(self, event):
        ''' 👉 https://quip.com/HrgkAuQCqBez#temp:C:bXDff3472e2ec4d4733bd1b38141 '''
        '''
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "Host": "iata.org",
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48"
        }
        '''
        dtfw.Msg(event)
    

    def HandleCheckout(self, event):
        ''' 👉 https://quip.com/HrgkAuQCqBez#temp:C:bXDca9dada42bf6431daed5f1c07 '''
        '''
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "Host": "iata.org",
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48"
        }
        '''
        dtfw.Msg(event)
    

    def HandleAbandon(self, event):
        ''' 👉 https://quip.com/HrgkAuQCqBez#temp:C:bXD2d6cd3790047405c89019c170 '''
        '''
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "Host": "iata.org",
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48"
        }
        '''
        dtfw.Msg(event)
    

    def HandleAssess(self, event):
        ''' 👉 https://quip.com/HrgkAuQCqBez#temp:C:bXD4396f26fefe34874a12828c36 '''
        '''
        "Body": {
            "QR": "🤝dtfw.org/QR,1,any-printer.com,7V8KD3G"
        }
        '''
        dtfw.Msg(event)
    

    def HandleGoodbye(self, event):
        ''' 👉 https://quip.com/HrgkAuQCqBez#temp:C:bXD9f09e5f058ee4fc8a77be4ebe '''
        '''
        "Body": {
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",
            "Message": "Parking ended for vehicle AB-12-34.".
        }
        '''
        dtfw.Msg(event)
    

    