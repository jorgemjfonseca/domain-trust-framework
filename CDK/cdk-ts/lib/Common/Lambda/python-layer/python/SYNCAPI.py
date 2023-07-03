# 📚 SYNCAPI

from DTFW import DTFW
dtfw = DTFW()


def test():
    return 'this is SYNCAPI test.'


class SYNCAPI:
    
    def Send(self, event: any): 

        msg = dtfw.Msg(event)
        msg.Stamp()
        envelope = msg.Envelope()

        sent = dtfw.Lambda('SENDER').Invoke(envelope)
        return sent
