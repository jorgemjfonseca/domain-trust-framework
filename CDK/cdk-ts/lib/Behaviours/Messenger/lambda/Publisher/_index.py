# 📚 Messenger-Publisher


def handler(event, context):
    from DTFW import DTFW
    return DTFW().MESSENGER().HandlePublisher(event)