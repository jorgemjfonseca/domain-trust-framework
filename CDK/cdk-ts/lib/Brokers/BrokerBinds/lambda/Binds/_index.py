# 📚 BrokerBinds-Binds

def handler(event, context):
    from DTFW import DTFW
    return DTFW().BROKER().Binds().HandleBinds(event)
