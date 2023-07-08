'''
📚 PUBLISHER
├─ handles Register(), Unregister(), and Subscribe()
│  └─ writes to Subscribers table 
├─ handles Updated()
│  ├─ writes to Updates table 
│  └─ sends to Messenger
└──handles Replay(), and Next()
    ├── reads from Updates table
    ├── writes to Tokens table
    └─ sends to Messenger
'''

import json
from HANDLER import HANDLER
from MSG import MSG
from DTFW import DTFW
from ITEM import ITEM
from STRUCT import STRUCT


# ✅ DONE
class PUBLISHER(DTFW, HANDLER):
    ''' 👉 https://quip.com/sBavA8QtRpXu/-Publisher '''


    # ✅ DONE
    def Updates(self):
        ''' 🪣 https://quip.com/sBavA8QtRpXu#temp:C:IEKd7992eec103b489a81b2576ca
        {
            "UpdateID": "8e8cb55b-55a8-49a5-9f80-439138e340a2", 
            "Domain": "example.com",
            "Timestamp": "2018-12-10T13:45:00.000Z"
        }'''
        return self.DYNAMO('Updates', keys=['UpdateID'])
    

    # ✅ DONE
    def Subscribers(self):
        ''' 🪣 https://quip.com/sBavA8QtRpXu#temp:C:IEKc08ac410e2ed414780eb190c8
        {
            "Domain": "example.com",
            "Filter": {}
        }'''
        return self.DYNAMO('Subscribers', keys=['Domain'])
    
    
    # ✅ DONE
    def Tokens(self):
        ''' 🪣 https://quip.com/sBavA8QtRpXu#temp:C:IEK3e519726b3b04dedbfbcb11e4 '''
        '''
        {
            "Token": "...",
            "Timestamp": "...",
            "Domain": "..."
        }
        '''
        return self.DYNAMO('Tokens', keys=['Token'])
    

    # ✅ DONE
    def HandleSubscribe(self, event):
        ''' 🐌 https://quip.com/sBavA8QtRpXu/-Publisher#temp:C:IEKf5f88769121840418de6755e4 '''

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
        msg = self.MSG(event)
        self.Subscribers().Upsert({
            "Domain": msg.From(),
            "Filter": msg.Att('Filter', default={})
        })


    # ✅ DONE
    def HandleUnsubscribe(self, event):
        ''' 🐌 https://quip.com/sBavA8QtRpXu#temp:C:IEK2b8247c67fae4d4487321c2e1 '''

        '''
        {
            "Header": {
                "From": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org"
            }
        }
        '''
        domain = self.MSG(event).From()
        self.Subscribers().Get(domain).Delete()


    # ✅ DONE
    def HandlePublish(self, event):
        ''' 🐌 https://quip.com/sBavA8QtRpXu/-Publisher#temp:C:IEK5a453bcdb55e4d41bcc57bbc6 
        {
            "Header": {
                "From": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org"
            }
        }
        '''
        msg = self.MSG(event)

        # TODO: this should be a DynamoDB stream event, to be more resilient.
        #   If the second step fails, a new UpdateID is inserted, growing to infinite.
        #   By separating the second step, it can fail independently with adding DB items.

        # save to Updates table.
        raw = {
            'UpdateID': self.UUID(),
            'Domain': msg.From(),
            'Timestamp': msg.Timestamp(),
            'Correlation': msg.Correlation()
        }
        update = self.TriggerLambdas('HandleEnrich@Publisher', raw)
        self.Updates().Upsert(update)

        # fan out to all subscribers.
        for subscriber in self.Subscribers().GetAll(): 
            if not self._ignore(update, subscriber):
                return self.SUBSCRIBER().InvokeUpdated(
                    update=update, 
                    to=subscriber.Require('Domain'))


    # ✅ DONE
    def _ignore(self, update, subscriber: ITEM):
         ''' 👉 Verify if the subscriber asked this to be filtered. '''
         payload = {
             'Update': update,
             'Subscriber': subscriber,
             'Ignore': False
         }

         result = self.TriggerLambdas(
             event=' HandleFilter@Publisher', 
             payload= payload)
         
         return result['Ignore']
             

    # ✅ DONE
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
        msg = self.MSG(replay)
        timestamp = msg.Require('Timestamp')
        
        # Verify if the requester is registered.
        domain = msg.From()
        subscriber = self.Subscribers().Get(domain)
        subscriber.Require()
        
        return self._replay(
            request=msg, 
            timestamp= timestamp, 
            subscriber= subscriber)


    # ✅ DONE
    def _replay(self, request:MSG, timestamp:str, subscriber=None, lastEvaluatedKey=None):
        ''' 🏃 Supports Replay() and Next().'''
        
        # TODO Don't send empty pages.
        #   Fill require to loop through the pages, or to set a filter().
        #   Actually, filters won't work because the filter is external on self._ignore().

        page = self.Updates().GetPageFromTimestamp(
            timestamp= timestamp, 
            lastEvaluatedKey= lastEvaluatedKey)

        items = []
        for item in page['Items']:
            update = {
                'UpdateID': item['ID'],
                'Domain': item['Domain'],
                'Timestamp': item['Timestamp']
            }
            if not self._ignore(update, subscriber):
                items.append(update)
        
        token = None
        if 'LastEvaluatedKey' in page:
            lastEvaluatedKey = page['LastEvaluatedKey']

            token = self.UUID()
            self.Tokens().Insert({
                'Token': token,
                'LastEvaluatedKey': json.dumps(lastEvaluatedKey),
                'TimeStamp': timestamp,
                'Domain': request.From()
            })

        self.SUBSCRIBER().InvokeConsume(
            request= request, 
            source= 'Publisher-Replay',
            updates= items,
            token= token)
    

    # ✅ DONE
    def InvokeNext(self, source:str, request:MSG, token:str):
        ''' 🏃 Invokes Next@Publisher'''
        self.MESSENGER().Push(
            source= source,
            to= request.From(),
            subject= 'Next@Publisher',
            body= {
                'Token': token
            }
        )


    # ✅ DONE
    def HandleNext(self, next):
        ''' 🐌 https://quip.com/sBavA8QtRpXu#temp:C:IEK9f614503f0d44441a02dcf37f 
        "Body": {
            "Token": "8e8cb55b-55a8-49a5-9f80-439138e340a2"
        }
        '''
        msg = self.MSG(next)

        # Check if the token belongs to this domain.
        token = self.Tokens().Get(msg)
        token.Match('Domain', msg.From())

        # Check if it's an active subscriber.
        subscriber = self.Subscribers().Get(msg.From())
        subscriber.Require()

        # Get the next updates
        lastEvaluatedKey = json.loads(token.Require('LastEvaluatedKey'))
        timestamp = token.Require('Timestamp')

        return self._replay(
            request= next, 
            timestamp= timestamp, 
            subscriber= subscriber,
            lastEvaluatedKey= lastEvaluatedKey)