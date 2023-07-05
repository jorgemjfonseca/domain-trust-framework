# 📚 Broker-Query

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Broker().Share().HandleQuery(event)
