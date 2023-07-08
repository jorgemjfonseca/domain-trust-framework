# 📚 SUBSCRIBER

# 👉 https://stackoverflow.com/questions/24853923/type-hinting-a-collection-of-a-specified-type
from typing import List, Set, Tuple, Dict


from ITEM import ITEM
from STRUCT import STRUCT
from MSG import MSG
from DTFW import DTFW
dtfw = DTFW()


def test():
    return 'this is SUBSCRIBER test.'


class SUBSCRIBER(DTFW):
    ''' 👉 https://quip.com/9ab7AO56kkxY/-Subscriber '''
    

    # ✅ DONE
    def InvokeUpdate(self, update:any, to:str):
        ''' 👉 https://quip.com/9ab7AO56kkxY#temp:C:ISdeb655f34cef549fbbb9669e4a '''
        
        return dtfw.MESSENGER().Push(
            source= 'Publisher-Filter',
            subject= 'Update@Subscriber',
            to= to,
            body= update)
    

    def HandleUpdate(self, event):
        ''' 👉 https://quip.com/9ab7AO56kkxY#temp:C:ISdeb655f34cef549fbbb9669e4a '''

        '''
        "Body": {
            "UpdateID": "8e8cb55b-55a8-49a5-9f80-439138e340a2",
            "Domain": "example.com",
            "Timestamp": "2018-12-10T13:45:00.000Z"
        }
        '''

        print(f'{event}')
        
        msg = dtfw.MSG(event)

        required = {
            'Publisher': msg.From(),
            'UpdateID': msg.Att('UpdateID', default= dtfw.Utils().UUID()), 
            'Timestamp': msg.Att('Timestamp', default= dtfw.Utils().Timestamp()),
            'TTL': dtfw.DYNAMO().TTL(days=1)
        }

        item = dtfw.Utils().Merge(
            msg.Body(),
            required
        ) 

        dtfw.DYNAMO('DEDUPS').Upsert(
            id= msg.Att('UpdateID'), 
            item= item)
        

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


    def HandleConsume(self, page):
        ''' 👉 https://quip.com/9ab7AO56kkxY#temp:C:ISd000c9e83bc4945b293024175e 
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

        # TODO Consider removing duplicates 
        # TODO Consider ignoring old updates

        '''
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
        print(f'{page}')

        list = dtfw.MSG(page)

        # Execute individual updates.
        for update in list.Body()['Updates']:
            single = dtfw.MSG()
            single.Header(list.Header())
            single.Body(update)
            self.HandleUpdate(single)

        # Ask for the next group of updates.
        if not list.IsMissingOrEmpty('Token'):
            self.Publisher().InvokeNext(
                token= list.Require('Token'),
                request= list,
                source='Subscriber-Consume')