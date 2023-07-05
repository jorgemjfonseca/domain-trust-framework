# 📚 Broker-Goodbye

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Broker().Sessions().HandleGoodbye(event)
