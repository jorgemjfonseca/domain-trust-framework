# 📚 Broker-Checkout

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Broker().Sessions().HandleCheckout(event)
