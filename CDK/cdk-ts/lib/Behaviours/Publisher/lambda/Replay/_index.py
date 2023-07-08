# 📚 Publisher-Replay


def handler(event, context):
    from DTFW import DTFW
    return DTFW().PUBLISHER().HandleReplay(event)