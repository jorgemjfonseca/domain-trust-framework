# 📚 Publisher-Updated

# 👉 https://quip.com/sBavA8QtRpXu/-Publisher#temp:C:IEK5a453bcdb55e4d41bcc57bbc6

from DYNAMO import DYNAMO
from SQS import SQS
from MSG import MSG
from UTILS import UTILS


updates = DYNAMO('UPDATES')


def handler(event, context):
    print(f'{event}')

    msg = MSG(event)
    domain = msg.From()
    id = UTILS.UUID() 
    update = {
        'UpdateID': id,
        'Domain': domain,
        'Timestamp': msg.Timestamp()
    }
    
    updates.Merge(id, update)
    

'''
{
    "Header": {
        "From": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org"
    }
}
'''