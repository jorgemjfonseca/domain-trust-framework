# 📚 Broker-QR

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Broker().Setup().HandleQR(event)
