# 📚 Publisher-Unsubscribe


def handler(event, context):
    from DTFW import DTFW
    return DTFW().PUBLISHER().HandleUnsubscribe(event)