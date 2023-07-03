# 📚 Publisher-Subscribe


def handler(event, context):
    from DTFW import DTFW
    return DTFW().Publisher().HandleSubscribe(event)