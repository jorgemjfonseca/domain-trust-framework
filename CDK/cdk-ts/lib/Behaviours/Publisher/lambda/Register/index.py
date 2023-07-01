# 📚 Publisher-Register

from PUBLISHER import PUBLISHER

def handler(event, context):
    return PUBLISHER._HandleRegister(event)
    