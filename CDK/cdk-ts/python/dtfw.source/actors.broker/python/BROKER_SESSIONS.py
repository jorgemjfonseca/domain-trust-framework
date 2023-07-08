
# 📚 BROKER_SESSIONS
      

from BROKER_SETUP import BROKER_SETUP
from DTFW import DTFW


class BROKER_SESSIONS(BROKER_SETUP, DTFW):
    ''' 👉 https://quip.com/HrgkAuQCqBez#bXDABAe5brB '''


    # ✅ DONE
    def Hosts(self): 
        ''' 👉 https://quip.com/HrgkAuQCqBez#temp:C:bXD380faa067708498dbbc554b36 '''
        return self.DYNAMO('HOSTS', keys=['WalletID', 'Host'])
    
    
    # ✅ DONE
    def Sessions(self): 
        ''' 👉 https://quip.com/HrgkAuQCqBez#temp:C:bXDdd6c1585433f4b6495262e8df '''
        return self.DYNAMO('SESSIONS', keys=['WalletID', 'Host', 'SessionID'])
    

    # ✅ DONE
    def HandleSessions(self, event):
        ''' 🚀 https://quip.com/HrgkAuQCqBez#temp:C:bXD09ae7595fe4943d5985d83fd0 '''
        '''
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a"
        }
        '''
        msg, wallet = self.VerifySignature(event)

        '''
        {
            "Hosts": [{
                "Host": "iata.org",    
                "Translation": "IATA",
                "Sessions": [{
                    "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",
                    "SessionTime": "2018-12-10T13:45:00.000Z"
                }]
            }]
        }
        '''
        return { 
            'Hosts': wallet.Att('Hosts', default=[])
        }


    # ✅ DONE
    def HandleTalker(self, event):
        ''' 🐌 https://quip.com/HrgkAuQCqBez#temp:C:bXDff3472e2ec4d4733bd1b38141 
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "Host": "iata.org",
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48"
        }
        '''
        msg, wallet = self.VerifySignature(event)

        self.HOST().InvokeTalker(
            source= 'Broker-Talker',
            to= msg.Require('Host'),
            sessionID= msg.Require('SessionID'))
            
    
    # ✅ DONE
    def HandleCheckout(self, event):
        ''' 🐌 https://quip.com/HrgkAuQCqBez#temp:C:bXDca9dada42bf6431daed5f1c07 '''
        '''
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "Host": "iata.org",
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48"
        }
        '''
        msg, wallet = self.VerifySignature(event)

        self.HOST().InvokeChekOut(
            source='Broker-Checkout', 
            to= msg.Require('Host'),
            sessionID= msg.Require('SessionID'))
    

    def HandleAbandon(self, event):
        ''' 🐌 https://quip.com/HrgkAuQCqBez#temp:C:bXD2d6cd3790047405c89019c170 '''
        '''
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "Host": "iata.org",
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48"
        }
        '''
        msg, wallet = self.VerifySignature(event)

        # For every vault in 🪣 Queries: 🤵📎 Broker. Share():
            # where session’s match
            # call 🐌 Suppress: 🗄️ Vault
        # Call 🐌 Abandoned: 🤗 Host on the host
        # Remove from 🪣 Sessions


    

    def HandleAssess(self, event):
        ''' 🚀 https://quip.com/HrgkAuQCqBez#temp:C:bXD4396f26fefe34874a12828c36 '''
        '''
        "Body": {
            "QR": "🤝dtfw.org/QR,1,any-printer.com,7V8KD3G"
        }
        '''
        self.MSG(event)
    

    def InvokeGoodbye(self, event):
        pass

    def HandleGoodbye(self, event):
        ''' 🐌 https://quip.com/HrgkAuQCqBez#temp:C:bXD9f09e5f058ee4fc8a77be4ebe '''
        '''
        "Body": {
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",
            "Message": "Parking ended for vehicle AB-12-34.".
        }
        '''
        self.MSG(event)
    

    