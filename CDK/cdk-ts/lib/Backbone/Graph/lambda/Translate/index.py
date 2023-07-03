# 📚 Graph-Translate

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Graph().HandleTranslate(event)
