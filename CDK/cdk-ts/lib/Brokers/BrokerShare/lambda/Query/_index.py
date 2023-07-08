# 📚 Broker-Query

def handler(event, context):
    from DTFW import DTFW
    return DTFW().BROKER().Share().HandleQuery(event)
