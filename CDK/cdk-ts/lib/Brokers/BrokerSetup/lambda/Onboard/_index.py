# 📚 Broker-Onboard

def handler(event, context):
    from DTFW import DTFW
    return DTFW().BROKER().Setup().HandleOnboard(event)
