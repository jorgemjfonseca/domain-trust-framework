# 📚 Notifier-Charge

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Notifier().HandleCharge(event)
