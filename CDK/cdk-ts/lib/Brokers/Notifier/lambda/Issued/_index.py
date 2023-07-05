# 📚 Notifier-Issued

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Notifier().HandleIssued(event)
