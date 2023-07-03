# 📚 SyncApiDkim-DkimSetterFn


def handler(event, context):
    from DTFW import DTFW
    return DTFW().SyncApi().Dkim().HandleDkimSetter(event)