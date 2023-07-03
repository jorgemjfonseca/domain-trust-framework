# 📚 SyncApiDkim-SecretSetter


def handler(event, context):
    from DTFW import DTFW
    return DTFW().SyncApi().Dkim().HandleSecretSetter(event)
