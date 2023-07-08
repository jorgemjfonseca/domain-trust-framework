# 📚 Broker-Sessions

def handler(event, context):
    from DTFW import DTFW
    return DTFW().BROKER().Sessions().HandleSessions(event)
