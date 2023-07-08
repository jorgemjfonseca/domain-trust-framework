# 📚 SYNCAPI

from MSG import MSG
from DTFW import DTFW
dtfw = DTFW()


def test():
    return 'this is SYNCAPI test.'


class SYNCAPI(DTFW):
    

    def Sender(self):
        from SENDER import SENDER as proxy
        return proxy()
    

    def Receiver(self):
        from RECEIVER import RECEIVER as proxy
        return proxy()
    

    def Dkim(self):
        from DKIM import DKIM as proxy
        return proxy()
    
    
    def Send(self, msg:MSG=None, to=None, body=None, subject=None): 

        if msg == None:
            msg = self.WRAP(to=to, body=body, subject=subject)

        msg.Stamp()
        envelope = msg.Envelope()

        sent = dtfw.LAMBDA('SENDER').Invoke(envelope)
        return sent



    def HandleSetAlias(self):
        import os
        r53 = dtfw.ROUTE53(os.environ['hostedZoneId'])

        r53.AddApiGW(
            customDomain = os.environ['customDomain'], 
            apiHostedZoneId = os.environ['apiHostedZoneId'],
            apiAlias = os.environ['apiAlias'])