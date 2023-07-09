# 📚 CODE

from ITEM import ITEM
from STRUCT import STRUCT


class RESOURCE(STRUCT):

    def Domain(self):
        return self.Require('Domain')
    
    def Locator(self):
        return self.Require('Locator')
    

class QR(RESOURCE):
    ''' 🔆 https://quip.com/zE0MAiuuPMaE/-NFC-QR '''


    def __init__(self, data):
        obj= data
        if isinstance(data, str):
            obj = self.Parse(data)
        super().__init__(obj)


    def Parse(self, string:str):
        ''' 🤝dtfw.org/QR,1,any-printer.com,7V8KD3G '''
        if not string.startswith('🤝'):
            raise Exception('Invalid QR, missing handshake!')
        
        parts = str.split(',')
        ret = {}
        ret['Code']= parts[0].replace('🤝')
        ret['Version']= parts[1]
        ret['Domain']= parts[2]
        ret['Locator']= parts[3]

        return ret


    def Code(self):
        return self.Require('Code')    
    

    def IsHostCode(self) -> bool:
        return self.Code() == 'dtfw.org/HOST'