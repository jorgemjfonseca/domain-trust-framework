# 📚 Publisher-Unsubscribe


def handler(event, context):
    from DTFW import DTFW
    return DTFW().Publisher().HandleUnsubscribe(event)