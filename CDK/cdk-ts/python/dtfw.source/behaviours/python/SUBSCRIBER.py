# 📚 SUBSCRIBER

# 👉 https://stackoverflow.com/questions/24853923/type-hinting-a-collection-of-a-specified-type
from typing import List, Set, Tuple, Dict

from ITEM import ITEM
from STRUCT import STRUCT
from MSG import MSG
from DTFW import DTFW



# ✅ DONE
class SUBSCRIBER(DTFW):
    ''' 👉 https://quip.com/9ab7AO56kkxY/-Subscriber '''
    

    # ✅ DONE
    def Dedups(self):
        ''' 🪣 https://quip.com/9ab7AO56kkxY#temp:C:ISd04f7e560d00b442f9efed03f1
        {
            "Publisher": "any.publisher.com",
            "UpdateID": "8e8cb55b-55a8-49a5-9f80-439138e340a2", 
            "Domain": "example.com",
            "Timestamp": "2018-12-10T13:45:00.000Z",
            "TTL": "2018-12-12T00:00:00.000Z"
        }
        '''
        return self.DYNAMO('DEDUPS', keys=['Publisher', 'UpdateID'])
    

    # ✅ DONE
    def InvokeUpdate(self, update:any, to:str):
        ''' 👉 https://quip.com/9ab7AO56kkxY#temp:C:ISdeb655f34cef549fbbb9669e4a '''
        
        return self.MESSENGER().Push(
            source= 'Publisher-Filter',
            subject= 'Update@Subscriber',
            to= to,
            body= update)
    

    # ✅ DONE
    def HandleUpdated(self, event):
        ''' 👉 https://quip.com/9ab7AO56kkxY#temp:C:ISdeb655f34cef549fbbb9669e4a 
        "Body": {
            "UpdateID": "8e8cb55b-55a8-49a5-9f80-439138e340a2",
            "Domain": "example.com",
            "Timestamp": "2018-12-10T13:45:00.000Z"
        }
        '''
        msg = self.MSG(event)
        self.Dedups().Upsert({
            'Publisher': msg.From(),
            'UpdateID': msg.Att('UpdateID', default= self.UUID()), 
            'Timestamp': msg.Att('Timestamp', default= self.Timestamp()),
            'TTL': self.DYNAMO().TTL(days=1),
            'Domain': msg.Require('Domain'),
        })
                

    # ✅ DONE
    def InvokeConsume(self, request:MSG, source:str, token:str, updates:List):
        ''' 👉 https://quip.com/9ab7AO56kkxY#temp:C:ISd000c9e83bc4945b293024175e '''

        body = {}
        body['Updates'] = updates
        if token:
            body['Token'] = token
            
        return self.MESSENGER().Push(
            subject= 'Consume@Subscriber',
            request= request, 
            to= request.From(),
            source= source,
            body= body)


    # ✅ DONE
    def HandleConsume(self, page):
        ''' 👉 https://quip.com/9ab7AO56kkxY#temp:C:ISd000c9e83bc4945b293024175e \n
        "Body": {
            "Updates":[
                {
                    "UpdateID": "8e8cb55b-55a8-49a5-9f80-439138e340a2",
                    "Domain": "example.com",
                    "Timestamp": "2018-12-10T13:45:00.000Z"
                }
            ],
            "Token": "cdaf19d8-3e51-4f1f-b5c7-2c7d9dda0c0d"
        }
        '''
        msg = self.MSG(page)

        # Execute individual updates.
        for update in msg.Body()['Updates']:
            single = self.WRAP(
                header= msg.Header(),
                body= update)
            self.HandleUpdated(single)

        # Ask for the next group of updates.
        if not msg.IsMissingOrEmpty('Token'):
            self.Publisher().InvokeNext(
                token= msg.Require('Token'),
                request= msg,
                source='Subscriber-Consume')