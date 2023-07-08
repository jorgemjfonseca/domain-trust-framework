# 📚 Graph-Identity


def handler(event, context):
    from DTFW import DTFW
    return DTFW().GRAPH().HandleIdentity(event)
