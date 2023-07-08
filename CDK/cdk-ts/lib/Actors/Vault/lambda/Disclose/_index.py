# 📚 Vault-Disclose


def handler(event, context):
    from DTFW import DTFW
    return DTFW().VAULT().HandleDisclose(event)