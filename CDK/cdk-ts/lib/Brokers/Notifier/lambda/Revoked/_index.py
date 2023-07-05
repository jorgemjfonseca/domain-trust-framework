# 📚 Notifier-Revoked

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Notifier().HandleRevoked(event)
