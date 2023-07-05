# 📚 Notifier-Updated

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Notifier().HandleUpdated(event)
