
def test():
    return 'this is SUBSCRIBER test.'


class SUBSCRIBER:


    @staticmethod
    def _HandlerConfirm(event):
        ''' 👉 https://quip.com/9ab7AO56kkxY#temp:C:ISd5cf963122f7a4faeb4e862c70 '''
        
        print(f'{event}')

        from MESSENGER import MESSENGER
        MESSENGER.Reply(
            request= event, 
            body= { "Confirmed": True },
            source= 'Subscriber-Confirm')
        

    @staticmethod
    def Consume(replay, items, token):

        consume = { 'Updates': items }
        if token:
            consume['Token'] = token

        from MESSENGER import MESSENGER
        MESSENGER.Reply(
            request= replay, 
            body= consume,
            source= 'Subscriber-Consume')


    @staticmethod
    def _HandleConsume(page):
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

        from MSG import MSG
        list = MSG(page)

        # Execute individual updates.
        for update in list.Body()['Updates']:
            single = MSG()
            single.Header(list.Header())
            single.Body(update)
            SUBSCRIBER._HandleUpdate(single)

        # Ask for the next group of updates.
        token = list.TryAtt('Token')
        if (token):
            from PUBLISHER import PUBLISHER
            PUBLISHER.Next(
                request= page, 
                token= token,
                source='Subscriber-Consume')


    @staticmethod
    def _HandleUpdate(event):
        ''' 👉 https://quip.com/9ab7AO56kkxY#temp:C:ISdeb655f34cef549fbbb9669e4a '''

        '''
        "Body": {
            "UpdateID": "8e8cb55b-55a8-49a5-9f80-439138e340a2",
            "Domain": "example.com",
            "Timestamp": "2018-12-10T13:45:00.000Z"
        }
        '''

        print(f'{event}')
        
        from MSG import MSG
        msg = MSG(event)
        body = msg.Body()

        id = body['UpdateID']

        from DYNAMO import DYNAMO
        required = {
            'Publisher': msg.From(),
            'UpdateID': body['UpdateID'], 
            'Timestamp': body['Timestamp'],
            'TTL': DYNAMO.TTL(days=1)
        }

        from UTILS import UTILS
        item = UTILS.Merge(
            body,
            required
        ) 

        table = DYNAMO('DEDUPS')
        table.Merge(id, item)
        