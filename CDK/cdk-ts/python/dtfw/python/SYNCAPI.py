# 📚 SYNCAPI

from DTFW import DTFW
dtfw = DTFW()


def test():
    return 'this is SYNCAPI test.'


class SYNCAPI:
    

    def Sender(self):
        from SENDER import SENDER as proxy
        return proxy()
    

    def Receiver(self):
        from RECEIVER import RECEIVER as proxy
        return proxy()
    

    def Dkim(self):
        from DKIM import DKIM as proxy
        return proxy()
    
    
    def Send(self, event: any): 

        msg = dtfw.Msg(event)
        msg.Stamp()
        envelope = msg.Envelope()

        sent = dtfw.Lambda('SENDER').Invoke(envelope)
        return sent



    def HandleSetAlias(self):
        import os
        r53 = dtfw.Route53(os.environ['hostedZoneId'])

        r53.AddApiGW(
            customDomain = os.environ['customDomain'], 
            apiHostedZoneId = os.environ['apiHostedZoneId'],
            apiAlias = os.environ['apiAlias'])