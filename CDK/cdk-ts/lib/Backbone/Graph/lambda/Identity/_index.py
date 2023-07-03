# 📚 Graph-Identity


def handler(event, context):
    from DTFW import DTFW
    return DTFW().Graph().HandleIdentity(event)
