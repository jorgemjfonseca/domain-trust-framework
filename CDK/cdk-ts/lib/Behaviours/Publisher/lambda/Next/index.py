# 📚 Publisher-Next

from PUBLISHER import PUBLISHER

def handler(event, context):
    return PUBLISHER._HandleNext(event)