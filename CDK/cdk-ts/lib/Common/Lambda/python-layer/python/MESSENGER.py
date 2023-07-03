# 📚 MESSENGER

from DTFW import DTFW
dtfw = DTFW()


def test():
    return 'this is MESSENGER test.'


class MESSENGER:
    

    def _publish(self, event:any, source:str, to:str=None):
        
        msg = dtfw.Msg(event)

        # Validate if there's a destination domain.
        if (to):
            msg.To(to)
        else:
            to = msg.To()

        # Send
        detailType = msg.Subject()
        envelope = msg.Envelope()
        
        dtfw.Bus().Publish(
            eventBusName= 'Messenger-Bus', 
            source= source,
            detailType= detailType, 
            detail= envelope)
        

    def Send(self, outbound:any, source:str, to:str=None):
        self._publish(outbound, source, to)
        
    
    def Reply(self, request: any, body:any, source:str):
        
        req = dtfw.Msg(request)
        to = req.From()

        out = dtfw.Msg()
        out.Wrap(to, body)
        out.Request(req.Envelope())

        self._publish(out, source)


    def HandlePublisher(self, event):
        print(f'{event=}')

        self._publish(
            event, 
            source= 'Messenger-Publisher')


    # 👉️ https://quip.com/NiUhAQKbj7zi
    def HandleSender(self, event):
        print(f'{event=}')

        msg = dtfw.Msg(event)
        msg.Stamp()
        envelope = msg.Envelope()
        
        return dtfw.SyncApi().Send(envelope)

    '''
    { 
        "Header": {
            "To": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org",
            "Subject": "AnyMethod"
        }
    }
    ''' 