# 📚 BrokerPay-Charge

def handler(event, context):
    from DTFW import DTFW
    return DTFW().BROKER().Pay().HandleCharge(event)
