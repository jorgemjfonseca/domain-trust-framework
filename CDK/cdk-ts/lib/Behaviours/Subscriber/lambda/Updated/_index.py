# 📚 Subscriber-Updated


def handler(event, context):
    from DTFW import DTFW
    return DTFW().SUBSCRIBER().HandleUpdated(event)