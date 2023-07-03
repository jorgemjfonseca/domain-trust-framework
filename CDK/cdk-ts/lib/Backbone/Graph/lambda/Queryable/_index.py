# 📚 Graph-Queryable

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Graph().HandleQueryable(event)
