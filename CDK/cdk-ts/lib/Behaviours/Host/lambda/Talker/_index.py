# 📚 Host-Talker


def handler(event, context):
    from DTFW import DTFW
    return DTFW().HOST().HandleTalker(event)