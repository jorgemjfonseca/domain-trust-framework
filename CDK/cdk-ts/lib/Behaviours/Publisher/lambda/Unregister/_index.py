# 📚 Publisher-Unregister


def handler(event, context):
    from DTFW import DTFW
    return DTFW().Publisher().HandleUnregister(event)