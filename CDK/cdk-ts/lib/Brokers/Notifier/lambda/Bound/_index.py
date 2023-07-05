# 📚 Notifier-Bound

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Notifier().HandleBound(event)
