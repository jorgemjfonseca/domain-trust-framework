# 📚 Broker-Replace

def handler(event, context):
    from DTFW import DTFW
    return DTFW().BROKER().Setup().HandleReplace(event)
