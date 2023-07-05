# 📚 HOST

def test():
    return 'this is HOST test.'

from DYNAMO import DYNAMO
from ITEM import ITEM
from MSG import MSG
from DTFW import DTFW

dtfw = DTFW()


class SESSION(ITEM):

    def Broker(self) -> str:
        return self.Require('Wallet.Broker')
    
    def WalletID(self) -> str:
        return self.Require('Wallet.WalletID')

    def MatchBroker(self, msg: MSG):
        self.Match('Wallet.Broker', msg.From())

    def Validate(self, msg: MSG):
        self.Require()
        self.MatchBroker(msg)



class HOST:


    def Sessions(self) -> DYNAMO:
        return dtfw.Dynamo('SESSIONS')
    def Session(self, sessionID) -> SESSION:
        session = self.Sessions().Get(sessionID)
        return SESSION(session)


    def fileKey(self, sessionID, fileID):
        return f'{sessionID}.{fileID}'
    def files(self) -> DYNAMO:
        return dtfw.Dynamo('FILES')
    def file(self, sessionID=None, fileID=None) -> ITEM:
        key = self.fileKey(sessionID, fileID)
        return dtfw.Item(self.files().Get(key))


    def ValidateSession(self, msg: MSG) -> ITEM:
        sessionID = msg.Require('SessionID')
        session = self.Session(sessionID)
        session.Validate(msg)
        


    def HandleAbandoned(self, event):
        ''' 👉 https://quip.com/s9oCAO3UR38A#temp:C:TDDbb2a3e48828a473b84c296777 '''
        '''
        "Body": {
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48"
        }
        '''
        msg = dtfw.Msg(event)
        session  = self.ValidateSession(msg)
        self.Sessions().Delete(session.Att('SessionID'))


    def HandleCheckIn(self, event):
        ''' 👉 https://quip.com/s9oCAO3UR38A#temp:C:TDDf29b75b2d0214f9a87224b338 '''
        '''
        "Body": {
            "Resource": {
                "Code": "dtfw.org/THING",
                "Locator": "MY-THING-ID"
            },
            "Wallet": {
                "Language": "en-us",    
                "Locator": "MY-WALLET"
                "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a"
            }
        }
        '''
        msg = dtfw.Msg(event)
        resource = msg.Require('Resource')
        wallet = msg.Require('Wallet')

        utils = dtfw.Utils()
        sessionID = utils.UUID()

        self.Sessions().Merge(
            id=sessionID, 
            item={
                'SessionID': sessionID,
                'Status': "CHECKING-IN",
                'CheckIn': utils.Merge(resource, {
                    'SessionTime': utils.Timestamp()
                }),
                'Wallet': utils.Merge(wallet, {
                    'Broker': msg.From()
                })
            })

        return { 'SessionID': sessionID }


    def HandleCheckOut(self, event):
        ''' 👉 https://quip.com/s9oCAO3UR38A#temp:C:TDD7b2a9a988f404282af7a63ff9 '''
        '''
        "Body": {
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48"
        }
        '''
        msg = dtfw.Msg(event)
        self.ValidateSession(msg)


    def HandleDownload(self, event):
        ''' 👉 https://quip.com/s9oCAO3UR38A#temp:C:TDD828d0b17f0fa414ba67fa5eab '''
        '''
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",    
            "FileID": "bc3d5f49-5d30-467a-9e0e-0cb5fd80f3cc"
        }
        '''
        msg = dtfw.Msg(event)
        self.ValidateSession(msg)
        
        file = self.file(
            sessionID= msg.Require('SessionID'),
            fileID= msg.Require('FileID'))
        file.Require()

        return {
            "Name": file.Require('Name'),
            "Serialized": file.Require('Serialized')
        }
        

    def HandleFound(self, event):
        ''' 👉 https://quip.com/s9oCAO3UR38A#temp:C:TDD558f6d6e0c8346e4bc9302b17 '''
        '''
        "Body": {
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",    
            "DeviceID": "MY-DEVICE",
            "Scanner": "heathrow.com"
        }
        '''
        msg = dtfw.Msg(event)
        self.ValidateSession(msg)


    def HandleTalker(self, event):
        ''' 👉 https://quip.com/s9oCAO3UR38A#temp:C:TDD7f08c68ca48949f19d0efc9bf '''
        '''
        "Body": {
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48"
        }
        '''
        msg = dtfw.Msg(event)
        self.ValidateSession(msg)


    def HandleUpload(self, event):
        ''' 👉 https://quip.com/s9oCAO3UR38A#temp:C:TDD35cfdaff99ec49bbb6bbba1f0 '''
        '''
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",        
            "Name": "a.jpg",
            "Serialized": "bisYfsHkJIyudS/O8FQOWpEdK"
        }
        '''
        msg = dtfw.Msg(event)
        self.ValidateSession(msg)

        utils = dtfw.Utils()
        fileID = utils.UUID()

        self.files().Merge(
            id= fileID, 
            item= utils.Merge(msg.Body(), {
                "FileID": fileID
            }))
