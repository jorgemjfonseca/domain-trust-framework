# 📚 Publisher-Register


def handler(event, context):
    from DTFW import DTFW
    return DTFW().Publisher().HandleRegister(event)
    