# 📚 Broker-QR

def handler(event, context):
    from DTFW import DTFW
    return DTFW().BROKER().Setup().HandleQR(event)
