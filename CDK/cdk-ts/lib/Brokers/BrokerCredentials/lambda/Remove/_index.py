# 📚 BrokerCredentials-Remove

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Broker().Credentials().HandleRemove(event)
