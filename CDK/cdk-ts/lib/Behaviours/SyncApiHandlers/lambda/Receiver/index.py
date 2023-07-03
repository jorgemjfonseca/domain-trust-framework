# 📚 SyncApiHandlers-ReceiverFn


def handler(event, context):
    from DTFW import DTFW
    DTFW().SyncApi().Receiver().Handle(event)