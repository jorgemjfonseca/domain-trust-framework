# 📚 Listener-Consume

from LISTENER import LISTENER

def handler(event, context):
    return LISTENER._HandleConsume(event)
