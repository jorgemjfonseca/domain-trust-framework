# 📚 BrokerBinds-Unbind

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Broker().Binds().HandleUnbind(event)
