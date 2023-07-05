# 📚 BrokerPay-Subscribe

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Broker().Pay().HandleSubscribe(event)
