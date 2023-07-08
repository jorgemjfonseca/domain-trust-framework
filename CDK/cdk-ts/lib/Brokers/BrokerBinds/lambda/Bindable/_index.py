# 📚 BrokerBinds-Bindable

def handler(event, context):
    from DTFW import DTFW
    return DTFW().BROKER().Binds().HandleBindable(event)
