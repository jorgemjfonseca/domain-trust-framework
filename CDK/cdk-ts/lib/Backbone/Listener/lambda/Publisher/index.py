# 📚 Listener-Publisher

from LISTENER import LISTENER

def handler(event, context):
    return LISTENER._HandlePublisher(event)

    