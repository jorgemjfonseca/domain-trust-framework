# 📚 Broker-Assess

def handler(event, context):
    from DTFW import DTFW
    return DTFW().BROKER().Sessions().HandleAssess(event)
