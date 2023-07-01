from MSG import MSG


def test():
    return 'this is MESSENGER test.'


class MESSENGER:
    

    @staticmethod
    def _publish(event:any, source:str, to:str=None):
        
        msg = MSG(event)

        # Validate if there's a destination domain.
        if (to):
            msg.To(to)
        else:
            to = msg.To()

        # Send
        detailType = msg.Subject()
        envelope = msg.Envelope()
        
        from BUS import BUS
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


    @staticmethod
    def _HandlePublisher(event):
        print(f'{event=}')

        MESSENGER._publish(
            event, 
            source= 'Messenger-Publisher')


    # 👉️ https://quip.com/NiUhAQKbj7zi
    @staticmethod
    def _HandleSender(event):
        print(f'{event=}')

        msg = MSG(event)
        msg.Stamp()
        envelope = msg.Envelope()
        
        from SYNCAPI import SYNCAPI
        sent = SYNCAPI.Send(envelope)
        return sent

    '''
    { 
        "Header": {
            "To": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org",
            "Subject": "AnyMethod"
        }
    }
    ''' 