# 📚 Publisher-Subscribe

# 👉 https://quip.com/sBavA8QtRpXu/-Publisher#temp:C:IEKf5f88769121840418de6755e4

import dtfw 

subscribers = dtfw.DYNAMO('SUBSCRIBERS')

def handler(event, context):
    print(f'{event}')

    msg = dtfw.MSG(event)
    domain = msg.From()
    filter = msg.Body()['Filter']
    
    subscribers.Upsert(domain, { 
        'Filter': filter,
        'Status': 'SUBSCRIBED'
    })
    

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