# 📚 Publisher-Unregister

# 👉 https://quip.com/sBavA8QtRpXu#temp:C:IEK2b8247c67fae4d4487321c2e1

from DYNAMO import DYNAMO
from MSG import MSG

subscribers = DYNAMO('SUBSCRIBERS')

def handler(event, context):
    print(f'{event}')

    domain = MSG(event).From()
    return subscribers.Delete(domain)
    

'''
{
    "Header": {
        "From": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org"
    }
}
'''