# 📚 Broker-Translate

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Broker().Setup().HandleTranslate(event)
