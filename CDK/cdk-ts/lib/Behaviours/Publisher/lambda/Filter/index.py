# 📚 Publisher-Filter


def handler(event, context):
    from DTFW import DTFW
    return DTFW().Publisher().HandleFilter(event)