# 📚 Listener-Consume

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Listener().HandleConsume(event)
