# 📚 MSG

# 👉 https://stackoverflow.com/questions/33533148/how-do-i-type-hint-a-method-with-the-type-of-the-enclosing-class
from __future__ import annotations

from STRUCT import STRUCT
from typing import Tuple

from DTFW import DTFW
dtfw = DTFW()


def test():
    return 'this is a MSG test.'


class MSG(STRUCT):
    ''' 👉 Structure of a message: { Header, Body, Hash, Signature }. '''
    
    def __init__(self, event={}):
        
        # instanciate the parent class: STRUCT
        super().__init__(event)
        
        # print in the beggining of all handlers.
        envelope = self.Envelope()
        print(f'MSG.Envelope()={envelope}')

        # set the Body as the root for the Att() method.
        self.SetAttRoot(self.Body())

        # map alias to the header.
        self.MapAtt('WalletID', 'Header.From')
        self.MapAtt('Host', 'Header.From')
        self.MapAtt('Broker', 'Header.From')
        self.MapAtt('Issuer', 'Header.From')
        self.MapAtt('Domain', 'Header.From')
    

    def Envelope(self) -> any:
        ''' 👉 Returns the internal envelope object. '''
        return super().Obj()
    

    def Header(self, header=None) -> STRUCT:
        ''' 👉 Gets or sets the Header. '''
        return super().Struct().RequireStruct('Header', set=header)


    def Subject(self, subject=None) -> str:
        ''' 👉 Gets or sets the Subject. '''
        return self.Header().RequireStr('Subject', set=subject)
        

    def From(self, set:str=None) -> str:
        ''' 👉 Gets or sets the From. '''
        return self.Header().RequireStr('From', set=set)
    

    def To(self, set:str=None) -> str:
        ''' 👉 Gets or sets the To. '''
        return self.Header().RequireStr('To', set=set)
    
    
    def Timestamp(self, set:str=None) -> str:
        ''' 👉 Gets or sets the Timestamp. '''
        return self.Header().RequireStr('Timestamp', set=set)
    

    def Correlation(self, set:str=None) -> str:
        ''' 👉 Gets or sets the Correlation. '''
        return self.Header().RequireStr('Correlation', set=set)
        

    def Body(self, body=None) -> STRUCT:
        ''' 👉 Updates or returns a copy of the body. '''
        envelope = self.Envelope()
        
        # setter
        if body:
            envelope['Body'] = body

        # existing getter, returns a copy
        if 'Body' in envelope and envelope['Body'] != '':
            return self.Copy().Struct('Body')
        
        # empty getter
        return STRUCT({})
    

    def Signature(self) -> str:
        ''' 👉 Gets the Signature. '''
        return self.RequireStr('Signature')
        

    def Hash(self) -> str:
        ''' 👉 Gets the Hash. '''
        return self.RequireStr('Hash')


    def Request(self, request:STRUCT) -> MSG:
        ''' 👉 Gets or sets the Header.Request. '''
        return MSG(self.Header().RequireStruct('Request', set=request))


    @staticmethod
    def Wrap(to: str, body: any, subject=None, header=None) -> MSG: 
        ''' 👉 Returns a stamped message, with header and body. '''

        ret = MSG({
            'Header': {
                'To': to,
                'Subject': subject
            },
            'Body': STRUCT.Unstruct(body)
        })

        if header != None:
            ret.Header(header)

        ret.Stamp()
        return ret


    def Stamp(self):
        ''' 👉 Adds correlation and timestamp. '''
        self.Header().DefaultGuid('Correlation')
        self.Header().DefaultTimestamp('Timestamp')
            

    
    def Canonicalize(self) -> str:
        ''' 👉️ https://bobbyhadz.com/blog/python-json-dumps-no-spaces '''
        copy = self.Copy()
        copy.RemoveAtt('Signature')
        copy.RemoveAtt('Hash')
        return copy.Canonicalize()
    

    def VerifyHeader(self):
        ''' 👉 Throws an exception if any of the header attributes are missing. '''
        msg = self
        msg.To()
        msg.Subject()
        msg.From()
        msg.Timestamp()
        msg.Correlation()


    def VerifySignature(self, publicKey: str):
        ''' 👉 Throws an exception if the Hash or Signature dont match the public key. '''
        
        validator = dtfw.SyncApi().Dkim().ValidateSignature(
            text = self.Canonicalize(), 
            publicKey = publicKey, 
            signature = self.Signature())

        expected = validator.Hash()
        received = self.Hash()
        
        isHashValid = (expected == received)
        print(f'Valid hash?: {isHashValid}')

        if not isHashValid:
            raise Exception(f'Wrong hash: expected [{expected}] but received [{received}]!')
        
        isVerified = validator['isVerified']
        print(f'Valid signature?: {isVerified}')

        if not isVerified:
            raise Exception(f'Invalid signature!')
        