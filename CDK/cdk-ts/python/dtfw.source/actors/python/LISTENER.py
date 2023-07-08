# 📚 LISTENER


from STRUCT import STRUCT
from ITEM import ITEM
from MSG import MSG
from PUBLISHER import PUBLISHER
from SUBSCRIBER import SUBSCRIBER


# ✅ DONE
class LISTENER(PUBLISHER, SUBSCRIBER):
    ''' 👂 https://quip.com/FCSiAU7Eku0X/-Listener '''
    
    
    # ✅ DONE
    def HandleEnricher(self, event):
        '''
        🐌 Updated: https://quip.com/FCSiAU7Eku0X/-Listener#temp:C:GLfc7d59b1cc13e4c4e89f85ba7f
        {
            'UpdateID': self.UUID(),
            'Domain': msg.From(),
            'Timestamp': msg.Timestamp(),
            'Correlation': "125a5c75-cb72-43d2-9695-37026dfcaa48"
        }
        🪣 https://quip.com/FCSiAU7Eku0X/-Listener#temp:C:GLf754341e1acba4cca8aa657b87
        {
            "Codes": [{
                "Code": "iata.org/SSR/WCHR"
            }]
        }
        '''
        msg = self.MSG(event)
        domain = msg.Require('Domain')

        manifest = self.DOMAIN(domain).FetchManifest()
        
        codes = []
        for code in manifest.Codes():
            codes.append[{
                'Code': domain + '/' + code.Require('Path')
            }]

        event['Codes'] = codes
        return event
    

    # ✅ DONE
    def HandleFilterer(self, event):
        # TODO: actually apply the filter -> requires the replay() not to send empty pages.
        '''
        {
             'Update': {},
             'Subscriber': {
                'Domain': 'example.com'
             },
             'Ignore': False
        }
        '''
        return {
            'Ignore': False
        }
    

    # ✅ DONE
    def HandleSubscriber(self, event):
        ''' 👉 https://quip.com/FCSiAU7Eku0X#temp:C:GLf6557997154774ed384f9db947 '''

        print(f'{event}')

        for update in self.DYNAMO().Records(event):
            msg = self.WRAP(body=update)
            msg.From(update['Domain'])
            self.HandlePublish(msg)