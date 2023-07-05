# 📚 BrokerBinds-Bindable

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Broker().Binds().HandleBindable(event)
