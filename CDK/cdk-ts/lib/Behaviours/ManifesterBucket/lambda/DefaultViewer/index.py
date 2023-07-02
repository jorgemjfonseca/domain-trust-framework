# 📚 ManifesterBucket-DefaultViewer

def handler(event, context):

    from MANIFEST import MANIFEST
    yaml = MANIFEST.RawAppConfig()
    
    from UTILS import UTILS
    return UTILS.HttpResponse(body=yaml, format='text')
