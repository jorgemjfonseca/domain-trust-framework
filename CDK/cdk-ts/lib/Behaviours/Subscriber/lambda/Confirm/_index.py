# 📚 Subscriber-Confirm


def handler(event, context):
    from DTFW import DTFW
    return DTFW().Subscriber().HandlerConfirm(event)