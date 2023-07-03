# 📚 Publisher-Next


def handler(event, context):
    from DTFW import DTFW
    return DTFW().Publisher().HandleNext(event)