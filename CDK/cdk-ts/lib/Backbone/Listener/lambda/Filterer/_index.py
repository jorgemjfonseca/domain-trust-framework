# 📚 Listener-Filterer

def handler(event, context):
    from DTFW import DTFW
    return DTFW().LISTENER().HandleFilterer(event)
