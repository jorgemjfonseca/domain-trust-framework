# 📚 Publisher-Updated


def handler(event, context):
    from DTFW import DTFW
    return DTFW().Publisher().HandleUpdated(event)
