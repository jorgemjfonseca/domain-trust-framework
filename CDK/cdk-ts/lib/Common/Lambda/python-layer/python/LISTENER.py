
# 📚 Listener: https://quip.com/FCSiAU7Eku0X/-Listener

def test():
    return 'this is SUBSCRIBER test.'

from DTFW import DTFW

class LISTENER:

    @staticmethod
    def _HandleConsume(event):
        # 👉 https://quip.com/FCSiAU7Eku0X#temp:C:GLfcf27fefa09924f62b4f449abb

        print(f'{event}')


    @staticmethod
    def _HandlePublisher(event):
        # 👉 https://quip.com/FCSiAU7Eku0X/-Listener

        print(f'{event}')

        update = {}

        from PUBLISHER import PUBLISHER
        PUBLISHER.Publish(update)


    @staticmethod
    def _HandleSubscribe(event):
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

        msg = DTFW.MSG(event)
        domain = msg.From()
        filter = msg.Body()['Filter']
        
        DTFW.DYNAMO('SUBSCRIBERS').Merge(domain, { 
            'Filter': filter,
            'Status': 'SUBSCRIBED'
        })


    @staticmethod
    def _HandleUpdated(event):
        # 👉 https://quip.com/FCSiAU7Eku0X#temp:C:GLfc7d59b1cc13e4c4e89f85ba7f
        
        print(f'{event}')
        
        from UTILS import UTILS
        id = UTILS.UUID() 

        msg = DTFW.MSG(event)
        
        update = {
            'UpdateID': id,
            'Domain': msg.From(),
            'Timestamp': msg.Timestamp()
        }

        DTFW.DYNAMO('UPDATES').Merge(id, update)
        
        DTFW.SQS('PUBLISHER').Send(update)