# 📚 BrokerBinds-Unbind

def handler(event, context):
    from DTFW import DTFW
    return DTFW().BROKER().Binds().HandleUnbind(event)
