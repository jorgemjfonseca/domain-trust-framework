# 📚 Listener-Publisher

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Listener().HandlePublisher(event)

    