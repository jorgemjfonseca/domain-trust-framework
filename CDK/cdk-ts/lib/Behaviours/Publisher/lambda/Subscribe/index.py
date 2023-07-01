# 📚 Publisher-Subscribe

from PUBLISHER import PUBLISHER

def handler(event, context):
    return PUBLISHER._HandleSubscribe(event)