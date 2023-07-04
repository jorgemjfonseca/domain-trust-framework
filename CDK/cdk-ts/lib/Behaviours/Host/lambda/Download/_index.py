# 📚 Host-Download


def handler(event, context):
    from DTFW import DTFW
    return DTFW().Host().HandleDownload(event)