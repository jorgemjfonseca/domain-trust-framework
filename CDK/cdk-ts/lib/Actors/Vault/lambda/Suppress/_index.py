# 📚 Vault-Supress


def handler(event, context):
    from DTFW import DTFW
    return DTFW().VAULT().HandleSupress(event)