# 📚 ManifesterAlerter.Alerter


def handler(event, context):
    from DTFW import DTFW
    return DTFW().Manifester().HandleAlerter(event)

