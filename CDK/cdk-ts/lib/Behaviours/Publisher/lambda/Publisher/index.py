# 📚 Publisher-Publisher

# 👉 https://quip.com/sBavA8QtRpXu/-Publisher


from DYNAMO import DYNAMO
from SQS import SQS
from MSG import MSG

subscribers = DYNAMO('SUBSCRIBERS')
fanout = SQS('FANOUT')

def handler(event, context):
    print(f'{event}')

    body = MSG(event).Body()
    for sub in subscribers.GetAll():
        to = sub['Domain']
        msg = MSG().Wrap(to, body)
        fanout.Send(msg)
