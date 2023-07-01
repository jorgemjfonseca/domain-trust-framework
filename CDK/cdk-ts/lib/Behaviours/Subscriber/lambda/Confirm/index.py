# 📚 Subscriber-Confirm

# 👉 https://quip.com/9ab7AO56kkxY#temp:C:ISd5cf963122f7a4faeb4e862c70

from MESSENGER import MESSENGER

def handler(event, context):
    print(f'{event}')

    MESSENGER.Reply(
        request= event, 
        body= { "Confirmed": True },
        source= 'Subscriber-Confirm')