# 📚 Listener-Subscribe

# 👉 https://quip.com/FCSiAU7Eku0X/-Listener#temp:C:GLf0d5cf021894d4b6babb7e0f4d

# Copied from Publisher-Subscribe


from DYNAMO import DYNAMO
from MSG import MSG

subscribers = DYNAMO('SUBSCRIBERS')

def handler(event, context):
    print(f'{event}')

    msg = MSG(event)
    domain = msg.From()
    filter = msg.Body()['Filter']
    
    subscribers.Merge(domain, { 
        'Filter': filter,
        'Status': 'SUBSCRIBED'
    })
    

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