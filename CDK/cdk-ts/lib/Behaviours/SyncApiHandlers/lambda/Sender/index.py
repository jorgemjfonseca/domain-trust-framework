# 📚 SyncApiHandlers-SenderFn


# 👉️ https://quip.com/NiUhAQKbj7zi
def handler(event, context):
    from DTFW import DTFW
    DTFW().SyncApi().Sender().Handle(event)