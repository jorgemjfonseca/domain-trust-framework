# 📚 Broker-Prompt

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Broker().Prompt().HandlePrompt(event)
