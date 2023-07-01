# 📚 Listener-Updated

# 👉 https://quip.com/FCSiAU7Eku0X#temp:C:GLfc7d59b1cc13e4c4e89f85ba7f


def handler(event, context):
    print(f'{event}')


from DYNAMO import DYNAMO
from SQS import SQS
from MSG import MSG
from UTILS import UTILS


updates = DYNAMO('UPDATES')
sqs = SQS('PUBLISHER')


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
    
    sqs.Send(update)
