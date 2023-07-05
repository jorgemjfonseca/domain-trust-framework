# 📚 Broker-Onboard

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Broker().Setup().HandleOnboard(event)
