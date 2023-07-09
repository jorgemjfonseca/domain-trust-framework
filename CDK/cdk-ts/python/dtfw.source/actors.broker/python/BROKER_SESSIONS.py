
# 📚 BROKER_SESSIONS
      

from BROKER_SETUP import BROKER_SETUP
from BROKER_SHARE import BROKER_SHARE
from DTFW import DTFW
from QR import QR
from MANIFEST import MANIFEST
from WALLET import WALLET


class BROKER_SESSIONS(BROKER_SETUP, BROKER_SHARE, DTFW):
    ''' 👉 https://quip.com/HrgkAuQCqBez#bXDABAe5brB '''


    # ✅ DONE
    def Hosts(self): 
        ''' 🪣 https://quip.com/HrgkAuQCqBez#temp:C:bXD380faa067708498dbbc554b36 
        {    
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "Host": "iata.org",
            "Translation": "IATA",
            "Language": "en-us"
        }
        '''
        return self.DYNAMO('HOSTS', keys=['WalletID', 'Host'])
    
    
    # ✅ DONE
    def Sessions(self): 
        ''' 👉 https://quip.com/HrgkAuQCqBez#temp:C:bXDdd6c1585433f4b6495262e8df 
        {    
            "Host": "iata.org",    
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",
            "SessionTime": "2018-12-10T13:45:00.000Z",
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a"
        }
        '''
        return self.DYNAMO('SESSIONS', keys=['Host', 'SessionID'])
    

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
            'Hosts': wallet.Hosts()
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
    

    # ✅ DONE
    def HandleAbandon(self, event):
        ''' 🐌 https://quip.com/HrgkAuQCqBez#temp:C:bXD2d6cd3790047405c89019c170 
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "Host": "iata.org",
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48"
        }
        '''
        msg, wallet = self.VerifySignature(event)

        sessionID = msg.Require('SessionID')
        host = msg.Require('Host')
        
        # 🪣 https://quip.com/rKzMApUS5QIi/-Broker-Share#temp:C:WTI65d339805abc4a79afae419df
        # For every vault in 🪣 Queries: 🤵📎 Broker.Share():
            # where session’s match
            # call 🐌 Suppress: 🗄️ Vault
        for vault in self.Queries().Get(msg).Structs['Vaults']:
            self.VAULT().InvokeSuppress(
                to= vault,
                consumer= host,
                sessionID= sessionID,
                source= 'Abandon@Broker'
            )

        # Call 🐌 Abandoned: 🤗 Host on the host
        self.HOST().InvokeAbandoned(
            source= 'Abandon@Broker',
            to= host,
            sessionID= sessionID
        )

        # Remove from 🪣 Sessions
        self.Sessions().Require(msg).Delete()

        # Remove from 🪣 Wallets
        wallet.RemoveSession(host= host, sessionID= sessionID)
    

    # ✅ DONE
    def HandleAssess(self, event):
        ''' 🧑‍🦰🚀 https://quip.com/HrgkAuQCqBez#temp:C:bXD4396f26fefe34874a12828c36 
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "QR": "🤝dtfw.org/QR,1,any-printer.com,7V8KD3G"
        }
        '''
        msg, wallet = self.VerifySignature(event)

        qr = self.QR(msg.Require('QR'))

        if qr.IsHostCode():
            self._handleSessionQR(qr=qr, wallet=wallet)
            
        else:
            raise Exception('Invalid QR')
        
        return {}


    # ✅ DONE
    def _handleSessionQR(self, qr:QR, wallet:WALLET):
        host = qr.Domain()
        language = wallet.Language()


        # Only pass the walletID to bound vaults.
        walletID = None
        if wallet.IsBoundToVault(host):
            walletID = wallet.ID()

        # Check-in into the host: 🚀 Check-in: 🤗 Host
        session = self.HOST().InvokeCheckIn(
            to= host,
            language= language,
            locator= wallet.Locator(),
            walletID= walletID
        )

        # Get the host’s name: 🚀 Identity: 🕸 Graph
        identity = self.GRAPH().InvokeIdentity(host)
        translation = identity.Translate(language)
        
        # Save to 🪣 Hosts
        self.Hosts().Upsert({
            "WalletID": wallet.ID(),
            "Host": host,
            "Translation": translation,
            "Language": language
        })

        # Save to: 🪣 Wallets
        wallet.AddSession(
            host=host, 
            sessionID=session.Att('SessionID'),
            translation= translation,
            language= language)
        
        self.NOTIFIER().InvokeUpdated(
            notifier= wallet.Notifier(), 
            walletID= wallet.ID(), 
            updates= ['SESSIONS'],
            source= 'Asssess@Broker')

    
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