# 📚 Graph-Queryable

def handler(event, context):
    from DTFW import DTFW
    return DTFW().GRAPH().HandleQueryable(event)
