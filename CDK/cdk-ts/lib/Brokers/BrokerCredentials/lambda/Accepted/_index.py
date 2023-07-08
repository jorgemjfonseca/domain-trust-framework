# 📚 BrokerCredentials-Accepted

def handler(event, context):
    from DTFW import DTFW
    return DTFW().BROKER().Credentials().HandleAccepted(event)
