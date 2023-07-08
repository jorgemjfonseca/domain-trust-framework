# 📚 LISTENER

# 📚 Listener: https://quip.com/FCSiAU7Eku0X/-Listener

def test():
    return 'this is SUBSCRIBER test.'


from STRUCT import STRUCT
from ITEM import ITEM
from MSG import MSG
from PUBLISHER import PUBLISHER

class LISTENER(PUBLISHER):


    # ✅ DONE
    def __init__(self):    
        self.On('HandleFilter@Publisher', self._filter)



    def _filter(self, update:STRUCT, subscriber:STRUCT, publish:bool):
        '''
        update= {
            "UpdateID": "8e8cb55b-55a8-49a5-9f80-439138e340a2",
            "Domain": "example.com",
            "Timestamp": "2018-12-10T13:45:00.000Z"
        }
        subscriber= {
            'Domain': ...
            'Filter': {
                "Conditions": [{
                    "Action": "INCLUDE",
                    "Query": "iata.org/SSR/*"
                }]
            }
        }
        '''
        pass


    def HandleConsume(self, event):
        # 👉 https://quip.com/FCSiAU7Eku0X#temp:C:GLfcf27fefa09924f62b4f449abb

        print(f'{event}')


    def HandlePublisher(self, event):
        # 👉 https://quip.com/FCSiAU7Eku0X/-Listener

        print(f'{event}')

        update = {}

        # TODO


    def HandleSubscribe(self, event):
        # 👉 https://quip.com/FCSiAU7Eku0X/-Listener#temp:C:GLf0d5cf021894d4b6babb7e0f4d

        '''
        {
            "Header": {
                "From": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org"
            }
            "Body": {
                "Filter": {
                    "Conditions": [{
                        "Action": "INCLUDE",
                        "Query": "iata.org/SSR/*"
                    }]
                }
            }
        }
        '''
        msg = self.MSG(event)        
        return self.Subscribers().Insert({ 
            'Domain': msg.From(),
            'Filter': msg.Att('Filter'),
            'Status': 'SUBSCRIBED'
        })


    def HandleUpdated(self, event):
        # 👉 https://quip.com/FCSiAU7Eku0X#temp:C:GLfc7d59b1cc13e4c4e89f85ba7f
        
        print(f'{event}')

        msg = self.MSG(event)
        id = self.UUID()
        update = {
            'UpdateID': id,
            'Domain': msg.From(),
            'Timestamp': msg.Timestamp()
        }

        self.DYNAMO('UPDATES').Upsert(id, update)
        
        # TODO: this should be an event of dynamo, to be ACID
        self.SQS('PUBLISHER').Send(update)