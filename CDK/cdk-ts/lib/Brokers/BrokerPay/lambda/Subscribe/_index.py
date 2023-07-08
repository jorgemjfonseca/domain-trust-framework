# 📚 BrokerPay-Subscribe

def handler(event, context):
    from DTFW import DTFW
    return DTFW().BROKER().Pay().HandleSubscribe(event)
