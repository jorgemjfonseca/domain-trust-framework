# 📚 Messenger-Sender


def handler(event, context):
    from DTFW import DTFW
    return DTFW().Messenger().HandleSender(event)