# 📚 BrokerCredentials-Revoke

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Broker().Credentials().HandleRevoke(event)
