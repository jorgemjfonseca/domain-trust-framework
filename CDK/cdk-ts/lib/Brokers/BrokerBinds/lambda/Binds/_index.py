# 📚 BrokerBinds-Binds

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Broker().Binds().HandleBinds(event)
