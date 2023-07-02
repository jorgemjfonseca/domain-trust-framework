# 📚 Publisher-Outbounder

from PUBLISHER import PUBLISHER

def handler(event, context):
    return PUBLISHER._HandleOutbounder(event)