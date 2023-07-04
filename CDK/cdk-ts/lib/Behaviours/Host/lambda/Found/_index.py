# 📚 Host-Found


def handler(event, context):
    from DTFW import DTFW
    return DTFW().Host().HandleFound(event)