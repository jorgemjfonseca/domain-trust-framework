# 📚 ManifesterBucket-DefaultViewer


def handler(event, context):
    from DTFW import DTFW
    return DTFW().Manifester().HandleDefaultViewer()