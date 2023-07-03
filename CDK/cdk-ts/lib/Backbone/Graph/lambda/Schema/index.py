# 📚 Graph-Schema

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Graph().HandleSchema(event)
