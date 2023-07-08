# 📚 Graph-Consume

def handler(event, context):
    from DTFW import DTFW
    return DTFW().GRAPH().HandleSubscriber(event)
