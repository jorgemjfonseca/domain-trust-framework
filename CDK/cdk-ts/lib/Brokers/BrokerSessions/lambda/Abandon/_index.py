# 📚 Broker-Abandon

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Broker().Sessions().HandleAbandon(event)
