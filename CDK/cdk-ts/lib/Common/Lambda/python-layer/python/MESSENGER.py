from UTILS import UTILS
from MSG import MSG
from BUS import BUS


def test():
    return 'this is MESSENGER test.'


class MESSENGER:
    

    @staticmethod
    def _publish(outbound:any, source:str, to:str=None):
        
        msg = MSG(outbound)

        # Validate if there's a destination domain.
        if (to):
            msg.To(to)
        else:
            to = msg.To()

        # Send
        detailType = msg.Subject()
        envelope = msg.Envelope()
        
        BUS.Publish(
            eventBusName= 'Messenger-Bus', 
            source= source,
            detailType= detailType, 
            detail= envelope)
        

    @staticmethod
    def Send(outbound:any, source:str, to:str=None):
        MSG._publish(outbound, source, to)
        
    
    @staticmethod
    def Reply(request: any, body:any, source:str):
        
        req = MSG(request)
        to = req.From()

        out = MSG()
        out.Wrap(to, body)
        out.Request(req.Envelope())

        MESSENGER._publish(out, source)