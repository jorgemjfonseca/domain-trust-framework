# 📚 Graph-Trusts

def handler(event, context):
    from DTFW import DTFW
    return DTFW().GRAPH().HandleTrusts(event)
