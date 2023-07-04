# 📚 Vault-Unbind


def handler(event, context):
    from DTFW import DTFW
    return DTFW().Vault().HandleUnbind(event)