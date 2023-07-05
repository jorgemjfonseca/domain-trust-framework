# 📚 BrokerCredentials-Credentials

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Broker().Credentials().HandleCredentials(event)
