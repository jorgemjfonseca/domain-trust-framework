# 📚 Notifier-Prompt

def handler(event, context):
    from DTFW import DTFW
    return DTFW().Notifier().HandlePrompt(event)
