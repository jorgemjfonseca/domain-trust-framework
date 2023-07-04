# 📚 Host-Abandoned


def handler(event, context):
    from DTFW import DTFW
    return DTFW().Host().HandleAbandoned(event)