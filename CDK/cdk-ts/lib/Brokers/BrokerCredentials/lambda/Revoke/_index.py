# 📚 BrokerCredentials-Revoke

def handler(event, context):
    from DTFW import DTFW
    return DTFW().BROKER().Credentials().HandleRevoke(event)
