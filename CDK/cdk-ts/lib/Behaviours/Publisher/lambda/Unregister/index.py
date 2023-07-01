# 📚 Publisher-Unregister

from PUBLISHER import PUBLISHER

def handler(event, context):
    return PUBLISHER._HandleUnregister(event)