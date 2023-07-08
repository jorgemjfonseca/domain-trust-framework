# 📚 Broker-Prompt

def handler(event, context):
    from DTFW import DTFW
    return DTFW().BROKER().Prompt().HandlePrompt(event)
