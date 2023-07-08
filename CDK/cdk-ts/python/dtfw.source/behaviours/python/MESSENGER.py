# 📚 MESSENGER

from DTFW import DTFW
from MSG import MSG
dtfw = DTFW()


def test():
    return 'this is MESSENGER test.'


class MESSENGER(DTFW):
    ''' 
    🐌 Messagenger behaviour of a domain. \n
    👉 https://quip.com/Fxj4AdnE6Eu5/-Messenger
    '''
    

    def _publish(self, data:any, source:str):
        ''' 👉 Publishes a message to the BUS. '''
        
        msg = dtfw.Msg(data)

        # Validate if there's a destination domain.
        msg.To()

        # Send
        detailType = msg.Subject()
        envelope = msg.Envelope()
        
        dtfw.Bus().Publish(
            eventBusName= 'Messenger-Bus', 
            source= source,
            detailType= detailType, 
            detail= envelope)
        

    def Send(self, msg:MSG, source:str):
        ''' 👉 Publishes a message to the BUS. '''
        self._publish(msg, source)


    def Push(self, source:str, to:str, body:any):
        ''' 👉 Publishes a message to the BUS. '''
        msg = self.Wrap(to=to, body=body)
        self._publish(msg, source=source)
        
    
    def Reply(self, req: MSG, body:any, source:str):
        
        to = req.From()

        out = dtfw.Wrap(to, body)
        out.Request(req)

        self._publish(out, source)


    def HandlePublisher(self, event):
        print(f'{event=}')

        self._publish(event, source= 'Messenger-Publisher')


    # 👉️ https://quip.com/NiUhAQKbj7zi
    def HandleSender(self, event):
        print(f'{event=}')

        msg = dtfw.Msg(event)
        msg.Stamp()
        
        return dtfw.SyncApi().Send(msg)

    '''
    { 
        "Header": {
            "To": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org",
            "Subject": "AnyMethod"
        }
    }
    ''' 