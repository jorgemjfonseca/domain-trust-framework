# 📚 Listener-Subscriber

def handler(event, context):
    from DTFW import DTFW
    return DTFW().LISTENER().HandleSubscriber(event)