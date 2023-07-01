# 📚 Publisher-Register

# 👉 https://quip.com/sBavA8QtRpXu/-Publisher#temp:C:IEKf5f88769121840418de6755e4

from DYNAMO import DYNAMO
from MSG import MSG

subscribers = DYNAMO('SUBSCRIBERS')

def handler(event, context):
    print(f'{event}')

    domain = MSG(event).From()
    
    subscribers.Merge(domain, {
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