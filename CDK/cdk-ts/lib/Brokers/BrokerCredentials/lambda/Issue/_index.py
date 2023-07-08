# 📚 BrokerCredentials-Issue

def handler(event, context):
    from DTFW import DTFW
    return DTFW().BROKER().Credentials().HandleIssue(event)
