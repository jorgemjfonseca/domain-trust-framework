# 📚 Graph-PublicKey

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Graph().HandlePublicKey(event)
