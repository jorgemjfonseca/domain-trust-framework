# 📚 BrokerCredentials-Accepted

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Broker().Credentials().HandleAccepted(event)
