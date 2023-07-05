# 📚 BrokerCredentials-Issue

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Broker().Credentials().HandleIssue(event)
