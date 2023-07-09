# 📚 HOST

from DTFW import DTFW
from HANDLER import HANDLER
from QR import QR, RESOURCE
from STRUCT import STRUCT
from UTILS import UTILS


# ✅ DONE
class HOST(DTFW, HANDLER, UTILS):
    ''' 🤗 https://quip.com/s9oCAO3UR38A/-Host \n
    Events:
     * HandleCheckOut@Host (optional)
     * HandleFound@Host (required)
     * HandleTalker@Host (required)
    '''


    # ✅ DONE
    def Sessions(self):
        ''' 🪣 https://quip.com/s9oCAO3UR38A#temp:C:TDD20456e042b3f43d49a73e0f92 
        {
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",
            "Status": "CHECKING-OUT",
            "CheckIn": {
                "SessionTime": "2018-12-10T13:45:00.000Z",
                "Code": "dtfw.org/THING",
                "Locator": "MY-THING-ID"
            },
            "Wallet": {
                "Language": "en-us",
                "Broker": "any-broker.com",
                "Locator": "MY-WALLET",
                "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a"
            }
        }
        '''
        return self.DYNAMO('SESSIONS', keys=['SessionID'])


    # ✅ DONE
    def Files(self):
        ''' 🪣 https://quip.com/s9oCAO3UR38A#temp:C:TDD026a3fce1988455796a1a4621 
        {
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",
            "FileID": "bc3d5f49-5d30-467a-9e0e-0cb5fd80f3cc",
            "Name": "a.jpg",
            "Serialized": "bisYfsHkJIyudS/O8FQOWpEdK"
        }
        '''
        return self.DYNAMO('FILES', keys=['SessionID', 'FileID'])
        

    # ✅ DONE
    def VerifyBrokerMsg(self, event):
        msg = self.MSG(event)
        session = self.Sessions().Get(msg.Body())
        session.Require('Wallet.Broker')
        session.Match('Wallet.Broker', msg.From())
        return msg, session
    

    # ✅ DONE
    def VerifyWalletMsg(self, event):
        msg = self.MSG(event)
        session = self.Sessions().Get(msg.Body())
        session.Require('Wallet.Locator')
        session.Match('Wallet.Locator', msg.Require('Locator'))
        return msg, session


    # ✅ DONE
    def InvokeAbandoned(self, source:str, to:str, sessionID:str):
        self.MESSENGER().Push(
            source=source, 
            to=to,
            subject= 'Abandoned@Host',
            body= { "SessionID": sessionID })
        

    # ✅ DONE
    def HandleAbandoned(self, event):
        ''' 🐌 https://quip.com/s9oCAO3UR38A#temp:C:TDDbb2a3e48828a473b84c296777 '''
        '''
        "Body": {
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48"
        }
        '''
        msg, session = self.VerifyBrokerMsg(event)
        session.Delete()


    # ✅ DONE
    def InvokeCheckIn(self, to:str, language:str, locator:str, walletID:str=None, resource={}) -> STRUCT:
        ''' 🤵🚀 https://quip.com/s9oCAO3UR38A#temp:C:TDDf29b75b2d0214f9a87224b338 '''

        body = { 
            "Resource": resource,
            "Wallet": {
                "Language": language,
                "Locator": locator,
                "WalletID": walletID
            }
        }
    
        if walletID != None:
            body['WalletID'] = walletID

        ret = self.SYNCAPI().Send(
            to=to,
            subject= 'CheckIn@Host',
            body= body)
        
        ''' { 
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48"
        }'''
        return ret
        
        
        
    # ✅ DONE
    def HandleCheckIn(self, event):
        ''' 🚀 https://quip.com/s9oCAO3UR38A#temp:C:TDDf29b75b2d0214f9a87224b338 
        "Body": {
            "Resource": {
                "Code": "dtfw.org/THING",
                "Locator": "MY-THING-ID"
            },
            "Wallet": {
                "Language": "en-us",    
                "Locator": "MY-WALLET",
                "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a"
            }
        }
        '''
        msg = self.MSG(event)
        resource = msg.Att('Resource', default={})
        wallet = msg.Require('Wallet')

        sessionID = self.UUID()

        self.Sessions().Insert({
            'SessionID': sessionID,
            'Status': "CHECKING-IN",
            'CheckIn': self.Merge(resource, {
                'SessionTime': self.Timestamp()
            }),
            'Wallet': self.Merge(wallet, {
                'Broker': msg.From()
            })
        })

        return { 'SessionID': sessionID }


    # ✅ DONE
    def InvokeChekOut(self, source:str, to:str, sessionID:str):
        self.MESSENGER().Push(
            source=source, 
            to=to,
            subject= 'ChekOut@Host',
            body= { "SessionID": sessionID })
        

    # ✅ DONE
    def HandleCheckOut(self, event):
        ''' 🐌 https://quip.com/s9oCAO3UR38A#temp:C:TDD7b2a9a988f404282af7a63ff9 '''
        '''
        "Body": {
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48"
        }
        '''
        msg, session = self.VerifyBrokerMsg(event)

        goodbye = { 'Goodbye': True }
        self.Trigger('HandleCheckOut@Host', event, goodbye)
        if goodbye['Goodbye']: 
            self.BROKER().InvokeGoodbye(event)
        

    # ✅ DONE
    def HandleDownload(self, event):
        ''' 🚀 https://quip.com/s9oCAO3UR38A#temp:C:TDD828d0b17f0fa414ba67fa5eab '''
        '''
        "Body": {
            "Locator": "ABCDEF",
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",    
            "FileID": "bc3d5f49-5d30-467a-9e0e-0cb5fd80f3cc"
        }
        '''
        msg, session = self.VerifyWalletMsg(event)
        self.Trigger('VerifyDownload@Host', msg, session)

        file = self.Files().Get(msg)

        return {
            "Name": file.Require('Name'),
            "Serialized": file.Require('Serialized')
        }
        

    # ✅ DONE
    def HandleFound(self, event):
        ''' 👉 https://quip.com/s9oCAO3UR38A#temp:C:TDD558f6d6e0c8346e4bc9302b17 '''
        '''
        "Body": {
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",    
            "DeviceID": "MY-DEVICE",
            "Scanner": "heathrow.com"
        }
        '''
        msg, session = self.VerifyBrokerMsg(event)
        self.Trigger('HandleFound@Host', event)


    # ✅ DONE
    def InvokeTalker(self, source:str, to:str, sessionID:str):
        self.MESSENGER().Push(
            source=source, 
            to=to,
            subject= 'Talker@Host',
            body= { "SessionID": sessionID })
        

    # ✅ DONE
    def HandleTalker(self, event):
        ''' 🐌 https://quip.com/s9oCAO3UR38A#temp:C:TDD7f08c68ca48949f19d0efc9bf 
        "Body": {
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48"
        }
        '''
        msg, session = self.VerifyBrokerMsg(event)
        self.Trigger('VerifyTalker@Host', msg, session)
        self.Trigger('HandleTalker@Host', event)


    # ✅ DONE
    def HandleUpload(self, event):
        ''' 👉 https://quip.com/s9oCAO3UR38A#temp:C:TDD35cfdaff99ec49bbb6bbba1f0 '''
        '''
        "Body": {
            "Locator": "ABCDEF",
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",        
            "Name": "a.jpg",
            "Serialized": "bisYfsHkJIyudS/O8FQOWpEdK"
        }
        '''
        msg, session = self.VerifyWalletMsg(event)
        self.Trigger('VerifyUpload@Host', msg, session)

        merge = msg.Body().Copy()
        merge.Merge({
            "FileID": self.UUID()
        })

        self.Files().Insert(merge)
