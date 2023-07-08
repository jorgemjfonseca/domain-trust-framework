# 📚 Broker-Translate

def handler(event, context):
    from DTFW import DTFW
    return DTFW().BROKER().Setup().HandleTranslate(event)
