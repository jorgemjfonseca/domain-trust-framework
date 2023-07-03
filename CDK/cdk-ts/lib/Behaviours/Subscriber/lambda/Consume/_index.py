# 📚 Subscriber-Consume


def handler(event, context):
    from DTFW import DTFW
    return DTFW().Subscriber().HandleConsume(event)