# 📚 BrokerPay-Charge

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Broker().Pay().HandleCharge(event)
