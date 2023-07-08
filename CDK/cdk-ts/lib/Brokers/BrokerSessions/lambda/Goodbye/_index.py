# 📚 Broker-Goodbye

def handler(event, context):
    from DTFW import DTFW
    return DTFW().BROKER().Sessions().HandleGoodbye(event)
