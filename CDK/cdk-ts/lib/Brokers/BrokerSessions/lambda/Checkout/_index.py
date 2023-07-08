# 📚 Broker-Checkout

def handler(event, context):
    from DTFW import DTFW
    return DTFW().BROKER().Sessions().HandleCheckout(event)
