# 📚 BrokerPay-Unsubscribe

def handler(event, context):
    from DTFW import DTFW
    return DTFW().BROKER().Pay().HandleUnsubscribe(event)
