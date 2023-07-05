# 📚 Notifier-Translated

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Notifier().HandleTranslated(event)
