# 📚 BrokerBinds-Bound

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Broker().Binds().HandleBound(event)
