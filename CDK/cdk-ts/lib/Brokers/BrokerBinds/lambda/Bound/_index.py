# 📚 BrokerBinds-Bound

def handler(event, context):
    from DTFW import DTFW
    return DTFW().BROKER().Binds().HandleBound(event)
