# 📚 Publisher-Publisher

from PUBLISHER import PUBLISHER

def handler(event, context):
    return PUBLISHER._HandlePublisher(event)
