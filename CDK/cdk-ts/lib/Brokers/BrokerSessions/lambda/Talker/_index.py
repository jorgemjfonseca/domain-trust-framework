# 📚 Broker-Talker

def handler(event, context):
    from DTFW import DTFW
    return DTFW().BROKER().Sessions().HandleTalker(event)
