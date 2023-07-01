# 📚 Publisher-Updated

# 👉 https://quip.com/sBavA8QtRpXu/-Publisher#temp:C:IEK5a453bcdb55e4d41bcc57bbc6

import dtfw 

updates = dtfw.DYNAMO('UPDATES')
sqs = dtfw.SQS('PUBLISHER')

def handler(event, context):
    print(f'{event}')

    msg = dtfw.MSG(event)
    domain = msg.From()
    update = {
        'UpdateID': dtfw.UUID(),
        'Domain': domain,
        'Timestamp': msg.Timestamp()
    }
    
    updates.Upsert(domain, update)
    
    sqs.Send(update)

    

'''
{
    "Header": {
        "From": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org"
    }
}
'''