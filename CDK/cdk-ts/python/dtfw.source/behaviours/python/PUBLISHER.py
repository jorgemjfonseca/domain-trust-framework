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

from MSG import MSG

def test():
    return 'this is PUBLISHER test.'


from DTFW import DTFW
dtfw = DTFW()

class PUBLISHER:
    ''' 👉 https://quip.com/sBavA8QtRpXu/-Publisher '''


    def Updates():
        ''' 👉 https://quip.com/sBavA8QtRpXu#temp:C:IEKd7992eec103b489a81b2576ca '''
        '''
        {
            "UpdateID": "8e8cb55b-55a8-49a5-9f80-439138e340a2", 
            "Domain": "example.com",
            "Timestamp": "2018-12-10T13:45:00.000Z"
        }
        '''
        return dtfw.Dynamo('UPDATES', keys=['UpdateID'])
    

    def Subscribers():
        ''' 👉 https://quip.com/sBavA8QtRpXu#temp:C:IEKd7992eec103b489a81b2576ca '''
        '''
        {
            "Domain": "example.com",
            "Filter": {}
        }
        '''
        return dtfw.Dynamo('SUBSCRIBERS', keys=['Domain'])
    

    def Tokens():
        ''' 👉 https://quip.com/sBavA8QtRpXu#temp:C:IEK3e519726b3b04dedbfbcb11e4 '''
        '''
        {
            "Token": "...",
            "Timestamp": "...",
            "Domain": "..."
        }
        '''
        return dtfw.Dynamo('Tokens', keys=['Token'])


    def HandleFilter(self, event):
        ''' 👉 https://quip.com/sBavA8QtRpXu/-Publisher '''

        print(f'{event}')

        msg = dtfw.Msg(event)

        return dtfw.Subscriber().InvokeUpdate(msg)
        
        
    

    def HandleNext(self, next):
        ''' 👉 https://quip.com/sBavA8QtRpXu#temp:C:IEK9f614503f0d44441a02dcf37f '''

        '''
        "Body": {
            "Token": "8e8cb55b-55a8-49a5-9f80-439138e340a2"
        }
        '''

        msg = dtfw.Msg(next)
        token = self.Tokens().Get(msg)

        token.Match('Domain', msg.From())
        lastEvaluatedKey = json.loads(token.Require('LastEvaluatedKey'))
        timestamp = token.Require('Timestamp')

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
        domain = dtfw.Msg(register).From()
        
        return self.Subscribers().Merge({
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
        msg = dtfw.Msg(replay)

        timestamp = msg.Require('Timestamp')
        
        return self._replay(
            request=msg, 
            timestamp= timestamp)


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
        msg = dtfw.Msg(event)
        
        return self.Subscribers().Merge({
            'Domain': msg.From(), 
            'Filter': msg.Att('Filter'),
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
        domain = dtfw.Msg(event).From()

        return self.Subscribers().Delete({
            "Domain": domain
        })


    def HandleUpdated(self, event):
        ''' 👉 https://quip.com/sBavA8QtRpXu/-Publisher#temp:C:IEK5a453bcdb55e4d41bcc57bbc6 '''

        '''
        {
            "Header": {
                "From": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org"
            }
        }
        '''
        msg = dtfw.Msg(event)

        # save to Updates table.
        self.Updates().Merge({
            'UpdateID': dtfw.Utils().UUID(),
            'Domain': msg.From(),
            'Timestamp': msg.Timestamp()
        })

        # fan out to all subscribers.
        for sub in self.Subscribers().GetAll(): 
            dtfw.Sqs('FILTER').Send(
                msg= dtfw.Wrap(
                    to= sub['Domain'], 
                    body= msg.Body()
                )
            )


    def _replay(self, request:MSG, timestamp:str, lastEvaluatedKey=None):
        
        page = self.Updates().GetPageFromTimestamp(timestamp, lastEvaluatedKey)

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

            token = dtfw.Utils().UUID()
            self.Tokens().Merge({
                'Token': token,
                'LastEvaluatedKey': json.dumps(lastEvaluatedKey),
                'TimeStamp': timestamp,
                'Domain': request.From()
            })

        body = { 'Updates': items }
        if token:
            body['Token'] = token

        return dtfw.Messenger().Reply(
            request= request, 
            body= body,
            source= 'Publisher-Replay')