# 📚 Broker-Sessions

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Broker().Sessions().HandleSessions(event)
