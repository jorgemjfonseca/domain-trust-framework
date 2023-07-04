# 📚 Host-CheckIn


def handler(event, context):
    from DTFW import DTFW
    return DTFW().Host().HandleCheckIn(event)