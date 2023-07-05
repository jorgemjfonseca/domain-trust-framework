# 📚 Notifier-Query

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Notifier().HandleQuery(event)
