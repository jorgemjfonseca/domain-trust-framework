# 📚 Vault-Continue


def handler(event, context):
    from DTFW import DTFW
    return DTFW().VAULT().HandleContinue(event)