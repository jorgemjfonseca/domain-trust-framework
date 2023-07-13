
# 📚 BROKER_SESSIONS
      
from BROKER_BINDS import BROKER_BINDS
from BROKER_SETUP import BROKER_SETUP
from BROKER_SHARE import BROKER_SHARE
from DTFW import DTFW
from MSG import MSG
from QR import QR
from MANIFEST import MANIFEST
from WALLET import WALLET


# ✅ DONE
class BROKER_SESSIONS(BROKER_SETUP, BROKER_SHARE, DTFW):
    ''' 🤵📎 https://quip.com/HrgkAuQCqBez#bXDABAe5brB '''


    # ✅ DONE
    def HandleSessions(self, event):
        ''' 🧑‍🦰🚀 https://quip.com/HrgkAuQCqBez#temp:C:bXD09ae7595fe4943d5985d83fd0 
        "Body": {}
        '''
        msg, wallet = self.VerifyWalletSignature(event)

        return { 
            "Sessions": [
                {
                    "ID": session.ID(),
                    "Host": session.HostDomain(),    
                    "HostTitle": session.HostTranslation(),
                    "SessionTime": session.SessionTime()
                }
                for session in self.SessionsOf(wallet) 
            ]
        }


    # ✅ DONE
    def HandleTalker(self, event):
        ''' 🧑‍🦰🐌 https://quip.com/HrgkAuQCqBez#temp:C:bXDff3472e2ec4d4733bd1b38141 
        "Body": {
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48"
        }
        '''
        msg, wallet = self.VerifyWalletSignature(event)

        session = self.GetSession(msg)
        session.MatchWalletID(msg)

        self.HOST().InvokeTalker(
            source= 'Broker-Talker',
            to= session.HostDomain(),
            sessionID= session.ID()
        )
            
    
    # ✅ DONE
    def HandleCheckout(self, event):
        ''' 🧑‍🦰🐌 https://quip.com/HrgkAuQCqBez#temp:C:bXDca9dada42bf6431daed5f1c07 '''
        '''
        "Body": {
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48"
        }
        '''
        msg, wallet = self.VerifyWalletSignature(event)

        session = self.GetSession(msg)
        session.MatchWalletID(msg)

        self.HOST().InvokeCheckOut(
            source='Broker-Checkout', 
            to= session.HostDomain(),
            sessionID= session.ID()
        )
    

    # ✅ DONE
    def HandleAssess(self, event):
        ''' 🧑‍🦰🚀 https://quip.com/HrgkAuQCqBez#temp:C:bXD4396f26fefe34874a12828c36 
        "Body": {
            "QR": "🤝dtfw.org/QR,1,any-printer.com,7V8KD3G"
        }
        '''
        msg, wallet = self.VerifyWalletSignature(event)

        qr = self.QR(msg.Require('QR'))

        if qr.IsHostCode():
            self._handleSessionQR(qr=qr, wallet=wallet)
            
        else:
            raise Exception('Invalid QR')
        
        return {}


    # ✅ DONE
    def _handleSessionQR(self, qr:QR, wallet:WALLET):

        host = qr.Domain()

        # Reuse any previous session to the same host.
        sessionID = None
        for session in self.SessionsOf(wallet):
            if session.HostDomain() == host:
                sessionID = session.ID()
                break

        # Check-in if there are no active sessions.
        if sessionID == None:
            sessionID = self._checkIn(qr=qr, wallet=wallet)

        # Request the initial options.
        self.HOST().InvokeTalker(
            source= 'Assess@Broker',
            to= host, 
            sessionID= sessionID
        )
        
    
    # ✅ DONE
    def _checkIn(self, qr:QR, wallet:WALLET) -> str:
        sessionID = self.UUID()
        host = qr.Domain()

        language = wallet.Language()
        binds = [ bind.ID() for bind in self.BindsOf(wallet) ]

        # Check-in into the host: 🚀 Check-in: 🤗 Host
        self.HOST().InvokeCheckIn(
            to= host,
            language= language,
            sessionID= sessionID,
            binds= binds,
            code= qr.Code(),
            locator= qr.Locator()
        )

        # Get the host’s name: 🚀 Identity: 🕸 Graph
        identity = self.GRAPH().InvokeIdentity(host)

        # Save to: 🪣 Wallets
        self.Sessions().Insert({   
            "ID": sessionID,
            "WalletID": wallet.ID(),
            "Host": host,    
            "Translation": identity.Translate(language),
            "SessionTime": self.Timestamp()
        })
    
        # Ask the UI to refresh the list.
        self.NOTIFIER().InvokeUpdated(
            wallet= wallet, 
            updates= ['SESSIONS'],
            source= 'Asssess@Broker')
        
        return sessionID


    # ✅ DONE
    def InvokeGoodbye(self, source:str, sessionID:str, message:str, to:str):
        ''' 🤗🐌 https://quip.com/HrgkAuQCqBez#temp:C:bXD9f09e5f058ee4fc8a77be4ebe '''
        self.MESSENGER().Push(
            source=source, 
            to= to, 
            subject= 'Goodbye@Broker',
            body={
                "SessionID": sessionID,
                "Message": message
            })


    # ✅ DONE
    def HandleGoodbye(self, event):
        ''' 🤗🐌 https://quip.com/HrgkAuQCqBez#temp:C:bXD9f09e5f058ee4fc8a77be4ebe 
        "Body": {
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",
            "Message": "Parking ended for vehicle AB-12-34.".
        }
        '''
        msg = self.MSG(event)
        session = self.GetSession(msg)
        session.MatchHost(msg)
        session.SuppressVaults(source= 'Goodbye@Broker')
        session.Delete()


    # ✅ DONE
    def HandleAbandon(self, event):
        ''' 🧑‍🦰🐌 https://quip.com/HrgkAuQCqBez#temp:C:bXD2d6cd3790047405c89019c170 
        "Body": {
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48"
        }
        '''
        msg, wallet = self.VerifyWalletSignature(event)

        session = self.GetSession(msg)
        session.MatchWalletID(msg)
        session.SuppressVaults(source='Abandon@Broker')
        session.Abandon(source='Abandon@Broker')
        session.Delete()
    