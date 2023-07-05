# 📚 BrokerPay-Resubscribe

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Broker().Pay().HandleResubscribe(event)
