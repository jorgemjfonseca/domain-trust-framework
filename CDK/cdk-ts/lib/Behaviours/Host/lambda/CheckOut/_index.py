# 📚 Host-CheckOut


def handler(event, context):
    from DTFW import DTFW
    return DTFW().HOST().HandleCheckOut(event)