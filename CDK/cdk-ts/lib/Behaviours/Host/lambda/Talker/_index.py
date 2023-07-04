# 📚 Host-Talker


def handler(event, context):
    from DTFW import DTFW
    return DTFW().Host().HandleTalker(event)