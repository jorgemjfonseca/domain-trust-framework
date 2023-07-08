# 📚 Listener-Enricher

def handler(event, context):
    from DTFW import DTFW
    return DTFW().LISTENER().HandleEnricher(event)
