# 📚 BrokerPay-Resubscribe

def handler(event, context):
    from DTFW import DTFW
    return DTFW().BROKER().Pay().HandleResubscribe(event)
