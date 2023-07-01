# 📚 Publisher-FanOuter

# 👉 https://quip.com/sBavA8QtRpXu/-Publisher

from MSG import MSG
from MESSENGER import MESSENGER

def handler(event, context):
    print(f'{event}')

    msg = MSG(event)
    msg.Subject('Subcriber-Update')
    MESSENGER.Send(msg, source='Publisher-FanOuter')
   