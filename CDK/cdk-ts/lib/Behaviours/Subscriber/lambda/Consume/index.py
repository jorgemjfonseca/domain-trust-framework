# 📚 Subscriber-Consume

from SUBSCRIBER import SUBSCRIBER

def handler(event, context):
    return SUBSCRIBER._HandleConsume(event)