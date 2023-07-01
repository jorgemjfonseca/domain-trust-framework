# 📚 Publisher-Replay

# 👉 https://quip.com/sBavA8QtRpXu/-Publisher#temp:C:IEK1a95aeba490844ce9168b7f4d

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
    },
    "Body": {
        "From": "2023-06-10T13:45:00.000Z"
    }
}
'''