# 📚 Host-Upload


def handler(event, context):
    from DTFW import DTFW
    return DTFW().HOST().HandleUpload(event)