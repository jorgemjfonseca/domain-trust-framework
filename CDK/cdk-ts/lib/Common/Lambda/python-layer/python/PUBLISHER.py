import json

def test():
    return 'this is PUBLISHER test.'


class PUBLISHER:
    
    # 🧪 FanOuter
    # 🧪 Publisher
    # 🧪 Register
    # 🧪 Unregister
    # 🧪 Replay
    # 🧪 Next
    # 🧪 Subscribe
    # 🧪 Updated

    @staticmethod
    def _HandleFanOuter(event):
        ''' 👉 https://quip.com/sBavA8QtRpXu/-Publisher '''

        print(f'{event}')

        from MSG import MSG
        msg = MSG(event)
        msg.Subject('Subcriber-Update')

        from MESSENGER import MESSENGER
        MESSENGER.Send(msg, source='Publisher-FanOuter')
    

    @staticmethod
    def _HandlePublisher(event):
        ''' 👉 https://quip.com/sBavA8QtRpXu/-Publisher 
        Read update stream and fan out to subscribers. '''

        print(f'{event}')

        # TODO: wrap out from DynamoDB strems

        from MSG import MSG
        body = MSG(event).Body()

        from SQS import SQS
        fanout = SQS('FANOUT')
        
        from DYNAMO import DYNAMO
        subscribers = DYNAMO('SUBSCRIBERS')

        for sub in subscribers.GetAll():
            to = sub['Domain']
            msg = MSG().Wrap(to, body)
            fanout.Send(msg)


    @staticmethod
    def _HandleRegister(register):
        ''' 👉 https://quip.com/sBavA8QtRpXu/-Publisher#temp:C:IEKf5f88769121840418de6755e4 '''

        '''
        {
            "Header": {
                "From": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org"
            }
        }
        '''
        print(f'{register}')

        from MSG import MSG
        domain = MSG(register).From()
        
        from DYNAMO import DYNAMO
        subscribers = DYNAMO('SUBSCRIBERS')
        subscribers.Merge(domain, {
            'Domain': domain,
            'Filter': {},
            'Status': 'REGISTERED'
        })


    @staticmethod
    def _HandleReplay(replay):
        ''' 👉 https://quip.com/sBavA8QtRpXu/-Publisher#temp:C:IEK1a95aeba490844ce9168b7f4d '''

        '''
        {
            "Header": {
                "From": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org"
            },
            "Body": {
                "From": "2023-06-10T13:45:00.000Z"
            }
        }
        '''
        print(f'{replay}')

        from MSG import MSG
        msg = MSG(replay)
        timestamp = msg.TryAtt('From')
        
        if not timestamp: 
            print(f'From not found, ignoring.')
            return
        
        return PUBLISHER._processReplay(replay, timestamp)
        

    @staticmethod
    def _processReplay(request, timestamp, lastEvaluatedKey=None):
        from DYNAMO import DYNAMO
        updates = DYNAMO('UPDATES')
        page = updates.GetPageFromTimestamp(timestamp, lastEvaluatedKey)

        items = []
        for item in page['Items']:
            items.append({
                'UpdateID': item['ID'],
                'Domain': item['Domain'],
                'Timestamp': item['Timestamp']
            })
        
        token = None
        if 'LastEvaluatedKey' in page:
            lastEvaluatedKey = page['LastEvaluatedKey']

            from UTILS import UTILS
            token = UTILS.UUID()

            tokens = DYNAMO('TOKENS')
            tokens.Merge(
                id=token, 
                item={ 
                    'LastEvaluatedKey': json.dumps(lastEvaluatedKey),
                    'TimeStamp': timestamp
                })

        from SUBSCRIBER import SUBSCRIBER
        return SUBSCRIBER.Consume(request, items, token)


    @staticmethod
    def Next(page, token, source):
        ''' 👉 https://quip.com/sBavA8QtRpXu/-Publisher#temp:C:IEK9f614503f0d44441a02dcf37f '''
        
        from MESSENGER import MESSENGER
        return MESSENGER.Reply(
            request= page,
            body= { 'Token': token },
            source= source)


    @staticmethod
    def _HandleNext(next):
        ''' 👉 https://quip.com/sBavA8QtRpXu#temp:C:IEK9f614503f0d44441a02dcf37f '''

        '''
        "Body": {
            "Token": "8e8cb55b-55a8-49a5-9f80-439138e340a2"
        }
        '''

        from MSG import MSG
        msg = MSG(next)
        token = msg.TryAtt('Token')
        if not token:
            print(f'Token not found, ignoring.')
            return

        from DYNAMO import DYNAMO
        tokens = DYNAMO('TOKENS')
        item = tokens.Get(token)
        lastEvaluatedKey = json.loads(item['LastEvaluatedKey'])
        timestamp = item['TimeStamp']

        return PUBLISHER._processReplay(next, timestamp, lastEvaluatedKey)


    @staticmethod
    def _HandleSubscribe(event):
        ''' 👉 https://quip.com/sBavA8QtRpXu/-Publisher#temp:C:IEKf5f88769121840418de6755e4 '''

        '''
        {
            "Header": {
                "From": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org"
            }
            "Body": {
                "Filter": {}
            }
        }
        '''
        print(f'{event}')
        
        from MSG import MSG
        msg = MSG(event)
        domain = msg.From()
        filter = msg.Body()['Filter']
        
        from DYNAMO import DYNAMO
        subscribers = DYNAMO('SUBSCRIBERS')
        subscribers.Merge(domain, { 
            'Filter': filter,
            'Status': 'SUBSCRIBED'
        })


    @staticmethod
    def _HandleUnregister(event):
        ''' 👉 https://quip.com/sBavA8QtRpXu#temp:C:IEK2b8247c67fae4d4487321c2e1 '''

        '''
        {
            "Header": {
                "From": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org"
            }
        }
        '''
        print(f'{event}')

        from MSG import MSG
        domain = MSG(event).From()

        from DYNAMO import DYNAMO
        subscribers = DYNAMO('SUBSCRIBERS')        
        return subscribers.Delete(domain)
    

    @staticmethod
    def _HandleUpdated(event):
        ''' 👉 https://quip.com/sBavA8QtRpXu/-Publisher#temp:C:IEK5a453bcdb55e4d41bcc57bbc6 '''

        '''
        {
            "Header": {
                "From": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org"
            }
        }
        '''
        print(f'{event}')

        from UTILS import UTILS
        id = UTILS.UUID() 

        from MSG import MSG
        msg = MSG(event)
        domain = msg.From()

        update = {
            'UpdateID': id,
            'Domain': domain,
            'Timestamp': msg.Timestamp()
        }

        from DYNAMO import DYNAMO
        updates = DYNAMO('UPDATES')
        updates.Merge(id, update)

