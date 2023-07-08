# 📚 Broker-Abandon

def handler(event, context):
    from DTFW import DTFW
    return DTFW().BROKER().Sessions().HandleAbandon(event)
