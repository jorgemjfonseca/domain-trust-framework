# 📚 SUBSCRIBER

from DTFW import DTFW
dtfw = DTFW()


def test():
    return 'this is SUBSCRIBER test.'


class SUBSCRIBER:


    def _HandlerConfirm(self, event):
        ''' 👉 https://quip.com/9ab7AO56kkxY#temp:C:ISd5cf963122f7a4faeb4e862c70 '''
        
        print(f'{event}')

        dtfw.Messenger().Reply(
            request= event, 
            body= { "Confirmed": True },
            source= 'Subscriber-Confirm')
        

    def Consume(self, replay, items, token):

        consume = { 'Updates': items }
        if token:
            consume['Token'] = token

        dtfw.Messenger().Reply(
            request= replay, 
            body= consume,
            source= 'Subscriber-Consume')


    def _HandleConsume(self, page):
        ''' 👉 https://quip.com/9ab7AO56kkxY#temp:C:ISd000c9e83bc4945b293024175e '''

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

        list = dtfw.Msg(page)

        # Execute individual updates.
        for update in list.Body()['Updates']:
            single = dtfw.Msg()
            single.Header(list.Header())
            single.Body(update)
            self._HandleUpdate(single)

        # Ask for the next group of updates.
        token = list.Att('Token')
        if (token):
            dtfw.Publisher().Next(
                request= page, 
                token= token,
                source='Subscriber-Consume')


    def _HandleUpdate(self, event):
        ''' 👉 https://quip.com/9ab7AO56kkxY#temp:C:ISdeb655f34cef549fbbb9669e4a '''

        '''
        "Body": {
            "UpdateID": "8e8cb55b-55a8-49a5-9f80-439138e340a2",
            "Domain": "example.com",
            "Timestamp": "2018-12-10T13:45:00.000Z"
        }
        '''

        print(f'{event}')
        
        msg = dtfw.Msg(event)

        required = {
            'Publisher': msg.From(),
            'UpdateID': msg.Att('UpdateID', default= dtfw.Utils().UUID()), 
            'Timestamp': msg.Att('Timestamp', default= dtfw.Utils().Timestamp()),
            'TTL': dtfw.Dynamo().TTL(days=1)
        }

        item = dtfw.Utils().Merge(
            msg.Body(),
            required
        ) 

        dtfw.Dynamo('DEDUPS').Merge(
            id= msg.Att('UpdateID'), 
            item= item)
        