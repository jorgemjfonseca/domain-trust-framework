# 📚 Messenger-Publisher

import os
import json
import dtfw

    
def handler(event, context):
    print(f'{event=}')

    msg = dtfw.MSG(event)
    return dtfw.BUS.Send(
        eventBusName= 'Messenger-Bus', 
        source= 'Messenger-Publisher',
        detailType= msg.Subject(), 
        detail= msg.Envelope())


'''

'''