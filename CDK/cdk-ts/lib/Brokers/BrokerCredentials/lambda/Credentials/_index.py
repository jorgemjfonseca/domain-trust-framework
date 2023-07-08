# 📚 BrokerCredentials-Credentials

def handler(event, context):
    from DTFW import DTFW
    return DTFW().BROKER().Credentials().HandleCredentials(event)
