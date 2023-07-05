'''
📚 PUBLISHER
├─ handles Register(), Unregister(), and Subscribe()
│  └─ writes to Subscribers table 
├─ handles Updated()
│  ├─ writes to Updates table 
│  └─ sends to Filter queue
│     └─ triggers Filter() function
│        └─ reads from Filters table
│           └─ loops each registered filterer function
│           │  └─ invokes function
│           └─ sends to Messenger
└──handles Replay(), and Next()
    ├── reads from Updates table
    ├── writes to Tokens table
    └── sends to Filter queue
        └─ triggers Filter() function...
'''

import json

def test():
    return 'this is PUBLISHER test.'


from DTFW import DTFW
dtfw = DTFW()

class PUBLISHER:

    def HandleFilter(self, event):
        ''' 👉 https://quip.com/sBavA8QtRpXu/-Publisher '''

        print(f'{event}')

        msg = dtfw.Msg(event)
        msg.Subject('Subcriber-Update')

        return dtfw.Messenger().Send(msg, source='Publisher-Filter')
    

    def HandleNext(self, next):
        ''' 👉 https://quip.com/sBavA8QtRpXu#temp:C:IEK9f614503f0d44441a02dcf37f '''

        '''
        "Body": {
            "Token": "8e8cb55b-55a8-49a5-9f80-439138e340a2"
        }
        '''

        token = dtfw.Msg(next).Att('Token')
        if not token:
            print(f'Token not found, ignoring.')
            return

        item = dtfw.Dynamo('TOKENS').ID(token)
        lastEvaluatedKey = json.loads(item['LastEvaluatedKey'])
        timestamp = item['TimeStamp']

        return self._replay(next, timestamp, lastEvaluatedKey)


    def HandleRegister(self, register):
        ''' 👉 https://quip.com/sBavA8QtRpXu/-Publisher#temp:C:IEKf5f88769121840418de6755e4 '''

        '''
        {
            "Header": {
                "From": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org"
            }
        }
        '''
        print(f'{register}')

        domain = dtfw.Msg(register).From()
        
        return dtfw.Dynamo('SUBSCRIBERS').Merge(domain, {
            'Domain': domain,
            'Filter': {},
            'Status': 'REGISTERED'
        })


    def HandleReplay(self, replay):
        ''' 👉 https://quip.com/sBavA8QtRpXu/-Publisher#temp:C:IEK1a95aeba490844ce9168b7f4d '''

        '''
        {
            "Header": {
                "From": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org"
            },
            "Body": {
                "Timestamp": "2023-06-10T13:45:00.000Z"
            }
        }
        '''
        print(f'{replay}')

        timestamp = dtfw.Msg(replay).Att('FrTimestampm')
        
        if not timestamp: 
            return { 'Alert': 'Timestamp not found, ignoring.' }

        return self._replay(replay, timestamp)


    def HandleSubscribe(self, event):
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
        
        msg = dtfw.Msg(event)
        domain = msg.From()
        filter = msg.Body()['Filter']
        
        return dtfw.Dynamo('SUBSCRIBERS').Merge(domain, { 
            'Filter': filter,
            'Status': 'SUBSCRIBED'
        })


    def HandleUnregister(self, event):
        ''' 👉 https://quip.com/sBavA8QtRpXu#temp:C:IEK2b8247c67fae4d4487321c2e1 '''

        '''
        {
            "Header": {
                "From": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org"
            }
        }
        '''
        print(f'{event}')

        domain = dtfw.Msg(event).From()

        return dtfw.Dynamo('SUBSCRIBERS').Delete(domain)


    def HandleUpdated(self, event):
        ''' 👉 https://quip.com/sBavA8QtRpXu/-Publisher#temp:C:IEK5a453bcdb55e4d41bcc57bbc6 '''

        '''
        {
            "Header": {
                "From": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org"
            }
        }
        '''
        print(f'{event}')

        msg = dtfw.Msg(event)

        # save to Updates table.
        dtfw.Dynamo('UPDATES').Merge(id, {
            'UpdateID': dtfw.Utils().UUID(),
            'Domain': msg.From(),
            'Timestamp': msg.Timestamp()
        })

        # fan out to all subscribers.
        for sub in dtfw.Dynamo('SUBSCRIBERS').GetAll(): 
            dtfw.Sqs('FILTER').Send(
                msg= dtfw.Msg().Wrap(
                    to= sub['Domain'], 
                    body= msg.Body()
                )
            )


    def _replay(self, request, timestamp, lastEvaluatedKey=None):
        
        page = dtfw.Dynamo('UPDATES').GetPageFromTimestamp(timestamp, lastEvaluatedKey)

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

            dtfw.Dynamo('TOKENS').Merge(
                id= dtfw.Utils().UUID(), 
                item= { 
                    'LastEvaluatedKey': json.dumps(lastEvaluatedKey),
                    'TimeStamp': timestamp
                })

        body = { 'Updates': items }
        if token:
            body['Token'] = token

        return dtfw.Messenger().Reply(
            request= request, 
            body= body,
            source= 'Publisher-Replay')