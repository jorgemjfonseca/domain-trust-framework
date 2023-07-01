# 📚 Messenger-SenderFn

import dtfw


def stampEnvelope(message: any):
    return dtfw.MSG(message).Stamp()


def sendEnvelope(envelope):
    return dtfw.LAMBDA('SENDER').Invoke(envelope)
   

# 👉️ https://quip.com/NiUhAQKbj7zi
def handler(event, context):
    print(f'{event=}')

    envelope = event
    stamped = stampEnvelope(envelope)
    sent = sendEnvelope(stamped)
    return sent
    

'''
{ 
    "Header": {
        "To": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org",
        "Subject": "AnyMethod"
    }
}
'''    