# 📚 Publisher-Register

# 👉 https://quip.com/sBavA8QtRpXu/-Publisher#temp:C:IEKf5f88769121840418de6755e4

import dtfw 

subscribers = dtfw.DYNAMO('SUBSCRIBERS')

def handler(event, context):
    print(f'{event}')

    domain = dtfw.MSG(event).From()
    
    subscribers.Upsert(domain, {
        'Domain': domain,
        'Filter': {},
        'Status': 'REGISTERED'
    })
    

'''
{
    "Header": {
        "From": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org"
    }
}
'''