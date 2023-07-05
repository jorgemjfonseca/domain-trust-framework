# 📚 Broker-Replace

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Broker().Setup().HandleReplace(event)
