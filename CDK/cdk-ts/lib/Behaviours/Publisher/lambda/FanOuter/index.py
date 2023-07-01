# 📚 Publisher-Register

# 👉 https://quip.com/sBavA8QtRpXu/-Publisher#temp:C:IEKf5f88769121840418de6755e4

import dtfw 


def handler(event, context):
    print(f'{event}')

    msg = dtfw.MSG(event)
    msg.Subject('Subcriber-Update')
    dtfw.MESSENGER.Send(
        envelope= msg.Envelope(), 
        source= 'Publisher-FanOuter'
    )
    

'''
{
    "Header": {
        "From": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org"
    }
}
'''