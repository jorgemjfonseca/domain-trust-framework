# 📚 BrokerPay-Unsubscribe

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Broker().Pay().HandleUnsubscribe(event)
