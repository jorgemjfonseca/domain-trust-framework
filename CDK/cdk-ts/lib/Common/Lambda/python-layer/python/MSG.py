from UTILS import UTILS


def test():
    return 'this is a MSG test.'


class MSG:
    
    
    def __init__(self, event={}):
        # check if it's a MSG object or a string.
        envelope = UTILS.TryCall(event, 'Envelope') 
        self._envelope = envelope


    def Envelope(self) -> any:
        return self._envelope

    
    def Copy(self) -> any:
        """ Returns a deep copy of the envelope. """
        return UTILS.Copy(self._envelope)
    

    def Header(self, header=None) -> any:
        if header:
            self._envelope['Header'] = header
        if 'Header' not in self._envelope:
            raise Exception(f'Header missing!')
        return self._envelope['Header']


    def Subject(self, subject=None) -> str:
        header = self.Header()
        if subject:
            header['Subject'] = subject        
        if 'Subject' not in header or header['Subject'].strip() == '':
            raise Exception(f'Header.Subject missing!')
        return header['Subject']
        

    def From(self) -> str:
        print(f'getHeaderFrom: {self._envelope=}')
        header = self.Header()
        if 'From' not in header or header['From'] == '':
            raise Exception(f'Header.From missing!')
        return header['From']
    

    def To(self) -> str:
        header = self.Header()
        if 'To' not in header or header['To'].strip() == '':
            raise Exception(f'Header.To missing!')
        return header['To']
    
    
    def Timestamp(self) -> str:
        header = self.Header()
        if 'Timestamp' not in header or header['Timestamp'].strip() == '':
            raise Exception(f'Header.Timestamp missing!')
        return header['Timestamp']
    

    def Correlation(self) -> str:
        header = self.Header()
        if 'Correlation' not in header or header['Correlation'].strip() == '':
            raise Exception(f'Header.Correlation missing!')
        return header['Correlation']
    
    
    def TryAtt(self, name:str, default = None) -> any:
        ''' Returns a copy of the attribute from the body, or None of it doesnt exist. '''
        body = self.Body()
        if name in body:
            return body[name]
        return default
    

    def GetAtt(self, name:str) -> any:
        ''' Returns a copy of the attribute from the body, or raises an exception. '''
        ret = self.TryAtt(name)
        if ret == None:
            raise Exception(f'Attribute not found: {name}')
        return ret


    def Body(self, body=None) -> any:
        ''' Updates or returns a copy of the body. '''
        if body:
            self._envelope['Body'] = body
        if 'Body' not in self._envelope or self._envelope['Body'] == '':
            #raise Exception(f'Body missing!')
            return {}
        if 'Body' in self._envelope:
            return self.Copy()['Body']
        return {}
    


    def Signature(self) -> str:
        #print(f'getSignature: {envelope=}')
        if 'Signature' not in self._envelope or self._envelope['Signature'].strip() == '':
            raise Exception(f'Signature missing!')
        return self._envelope['Signature']
        

    def Hash(self) -> str:
        #print(f'getHash: {envelope=}')
        if 'Hash' not in self._envelope:
            raise Exception(f'Hash missing!')
        return self._envelope['Hash']


    def Request(self, request) -> str:
        header = self.Request()
        if request:
            header['Request'] = request
        if 'Request' not in header:
            raise Exception(f'Request missing!')
        return header['Request']


    @staticmethod
    def Wrap(to: str, body) -> any:
        envelope =  {
            'Header': {
                'To': to
            },
            'Body': body
        }
        msg = MSG(envelope)
        msg.Stamp()
        return msg._envelope


    def Stamp(self) -> any:
        defaults = {
            'Header': {
                'Correlation': UTILS.Correlation(),
                'Timestamp': UTILS.Timestamp()
            },
            'Body': {}
        }
        print(f'{defaults=}')

        original = self.Envelope()
        stamped = defaults
        UTILS.Merge(stamped['Header'], original['Header']) 
        if 'Body' in original:
            UTILS.Merge(stamped['Body'], original['Body']) 

        self._envelope = stamped
        return stamped


    # 👉️ https://bobbyhadz.com/blog/python-json-dumps-no-spaces
    def Canonicalize(self) -> str:
        copy = UTILS.Copy(self._envelope)
        del copy['Signature']
        del copy['Hash']

        return UTILS.Canonicalize(copy)
    

    def ValidateHeader(self):
        msg = self.Envelope()
        msg.To()
        msg.Subject()
        msg.From()
        msg.Timestamp()
        msg.Correlation()