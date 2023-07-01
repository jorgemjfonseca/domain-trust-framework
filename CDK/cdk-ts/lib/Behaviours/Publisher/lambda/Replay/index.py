# 📚 Publisher-Replay

from PUBLISHER import PUBLISHER

def handler(event, context):
    return PUBLISHER._HandleReplay(event)