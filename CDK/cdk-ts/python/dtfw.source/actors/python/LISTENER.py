# 📚 LISTENER

# 📚 Listener: https://quip.com/FCSiAU7Eku0X/-Listener

def test():
    return 'this is SUBSCRIBER test.'


from DTFW import DTFW
dtfw = DTFW()

class LISTENER:


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
        print(f'{event}')

        # Copied from Publisher-Subscribe

        msg = dtfw.Msg(event)
        
        return dtfw.Dynamo('SUBSCRIBERS').Upsert(
            id= msg.From(), 
            item= { 
                'Filter': msg.Att('Filter'),
                'Status': 'SUBSCRIBED'
            })


    def HandleUpdated(self, event):
        # 👉 https://quip.com/FCSiAU7Eku0X#temp:C:GLfc7d59b1cc13e4c4e89f85ba7f
        
        print(f'{event}')

        msg = dtfw.Msg(event)
        id = dtfw.Utils.UUID()
        update = {
            'UpdateID': id,
            'Domain': msg.From(),
            'Timestamp': msg.Timestamp()
        }

        dtfw.Dynamo('UPDATES').Upsert(id, update)
        
        # TODO: this should be an event of dynamo, to be ACID
        dtfw.Sqs('PUBLISHER').Send(update)