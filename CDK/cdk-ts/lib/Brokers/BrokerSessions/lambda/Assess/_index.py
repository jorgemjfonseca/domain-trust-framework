# 📚 Broker-Assess

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Broker().Sessions().HandleAssess(event)
