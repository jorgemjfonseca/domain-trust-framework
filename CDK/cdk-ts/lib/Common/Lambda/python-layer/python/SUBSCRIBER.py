
def test():
    return 'this is SUBSCRIBER test.'


class SUBSCRIBER:


    @staticmethod
    def _HandlerConfirm(event):
        # 👉 https://quip.com/9ab7AO56kkxY#temp:C:ISd5cf963122f7a4faeb4e862c70
        
        print(f'{event}')

        from MESSENGER import MESSENGER

        MESSENGER.Reply(
            request= event, 
            body= { "Confirmed": True },
            source= 'Subscriber-Confirm')
        

    @staticmethod
    def _HandleConsume(event):
        # 👉 https://quip.com/9ab7AO56kkxY#temp:C:ISd000c9e83bc4945b293024175e

        print(f'{event}')
    
        # TODO


    @staticmethod
    def _HandleUpdate(event):
        # 👉 https://quip.com/9ab7AO56kkxY#temp:C:ISdeb655f34cef549fbbb9669e4a

        '''
        "Body": {
            "UpdateID": "8e8cb55b-55a8-49a5-9f80-439138e340a2",
            "Domain": "example.com",
            "Timestamp": "2018-12-10T13:45:00.000Z"
        }
        '''

        print(f'{event}')

        from DYNAMO import DYNAMO
        from MSG import MSG
        from UTILS import UTILS

        table = DYNAMO('DEDUPS')
        
        msg = MSG(event)
        body = msg.Body()

        id = body['UpdateID']

        item = UTILS.Merge(
            body,
            {
                "Publisher": msg.From(),
                "UpdateID": body['UpdateID'], 
                "Timestamp": body['Timestamp'],
                "TTL": DYNAMO.TTL(days=1)
            }
        ) 

        table.Merge(id, item)
        