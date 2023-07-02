# 📚 ManifesterBucket-YamlViewer

def handler(event, context):

    from MANIFEST import MANIFEST
    manifest = MANIFEST.FromAppConfig()
    
    from UTILS import UTILS
    return UTILS.HttpResponse(body=manifest, format='yaml')
