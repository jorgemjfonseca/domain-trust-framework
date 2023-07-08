# 📚 BrokerCredentials-Remove

def handler(event, context):
    from DTFW import DTFW
    return DTFW().BROKER().Credentials().HandleRemove(event)
