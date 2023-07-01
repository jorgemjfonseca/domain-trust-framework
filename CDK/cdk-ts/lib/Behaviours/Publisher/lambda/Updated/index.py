# 📚 Publisher-Updated

from PUBLISHER import PUBLISHER

def handler(event, context):
    return PUBLISHER._HandleUpdated(event)
