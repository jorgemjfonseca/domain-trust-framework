# 📚 Vault-Bind


def handler(event, context):
    from DTFW import DTFW
    return DTFW().VAULT().HandleBind(event)