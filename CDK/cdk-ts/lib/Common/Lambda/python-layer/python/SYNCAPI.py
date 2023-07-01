import os

def test():
    return 'this is SYNCAPI test.'


class SYNCAPI:
    
    @staticmethod
    def Send(event: any): 
        from MSG import MSG
        from LAMBDA import LAMBDA

        msg = MSG(event)
        msg.Stamp()
        envelope = msg.Envelope()

        sent = LAMBDA('SENDER').Invoke(envelope)
        return sent
