# 📚 Notifier-Onboard

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Notifier().HandleOnboard(event)
