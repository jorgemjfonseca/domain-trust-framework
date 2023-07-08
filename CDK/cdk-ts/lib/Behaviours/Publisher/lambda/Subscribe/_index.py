# 📚 Publisher-Subscribe


def handler(event, context):
    from DTFW import DTFW
    return DTFW().PUBLISHER().HandleSubscribe(event)