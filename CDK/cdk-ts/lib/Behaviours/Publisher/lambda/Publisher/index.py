# 📚 Publisher-Register

# 👉 https://quip.com/sBavA8QtRpXu/-Publisher#temp:C:IEKf5f88769121840418de6755e4

import dtfw 

subscribers = dtfw.DYNAMO('SUBSCRIBERS')
fanout = dtfw.SQS('FANOUT')

def handler(event, context):
    print(f'{event}')

    body = dtfw.MSG(event).Body()
    for sub in subscribers.GetAll():
        to = sub['Domain']
        msg = dtfw.MSG.Wrap(to, body)
        fanout.Send(msg)
    

'''
{
    "Header": {
        "From": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org"
    }
}
'''