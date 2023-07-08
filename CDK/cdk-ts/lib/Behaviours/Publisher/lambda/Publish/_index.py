# 📚 Publisher-Updated


def handler(event, context):
    from DTFW import DTFW
    return DTFW().PUBLISHER().HandlePublish(event)
