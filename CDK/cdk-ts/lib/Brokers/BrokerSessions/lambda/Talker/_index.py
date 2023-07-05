# 📚 Broker-Talker

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Broker().Sessions().HandleTalker(event)
