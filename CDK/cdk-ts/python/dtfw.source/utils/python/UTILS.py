# 📚 UTILS


def test():
    return 'this is a UTILS test.'


class NotFoundException(Exception):
    pass

class InvalidRequestException(Exception):
    pass


from WEB import WEB
from YAML import YAML

class UTILS(WEB, YAML): 


    def Timer(self):
        from TIMER import TIMER as proxy
        return proxy()


    def STRUCT(self, obj):
        ''' 👉 Wraps an object with a STRUCT. '''
        from STRUCT import STRUCT
        return STRUCT(obj=obj)
    

    def Unstruct(self, obj):
        ''' 👉 If the object is a STRUCT, returns the inner object. '''
        from STRUCT import STRUCT
        return STRUCT.Unstruct(obj=obj)


    def RaiseNotFoundException(self):
        raise NotFoundException
    

    def RaiseInvalidRequestException(self):
        raise InvalidRequestException
    



    def Copy(self, obj):        
        from copy import deepcopy
        return deepcopy(obj)
    

    def UUID(self):
        ''' 👉️ https://stackoverflow.com/questions/37049289/how-do-i-convert-a-python-uuid-into-a-string '''
        import uuid
        return str(uuid.uuid4());
    
    
    def Correlation(self):
        ''' 👉️ https://quip.com/NiUhAQKbj7zi#temp:C:XAYf6d35adc1f4e4f0795954ef86 '''
        correlation = self.UUID();
        print(f'{correlation=}')
        return correlation


    def Timestamp(self):
        ''' 👉️ Returns a current date-time in UTC format.
        https://stackoverflow.com/questions/53676600/string-formatting-of-utcnow '''
        import datetime
        timestamp = datetime.datetime.utcnow().isoformat() + 'Z'
        return timestamp


    def Canonicalize(self, object: any) -> str:
        ''' 👉️ https://bobbyhadz.com/blog/python-json-dumps-no-spaces '''
        import json
        canonicalized = json.dumps(object, separators=(',', ':'))
        print(f'{canonicalized=}')
        return canonicalized
    

    
    def TryCall(self, obj, name):
        '''  👉️ https://bobbyhadz.com/blog/python-check-if-object-has-method#check-if-an-object-has-a-specific-method-in-python '''
        method = getattr(obj, name, None)
        if callable(method):
            return method()
        return obj


    def Merge(self, obj1, obj2):
        ''' 👉️ https://stackoverflow.com/questions/14839528/merge-two-objects-in-python '''
        if obj1 == None:
            return obj2
        if obj2 == None:
            return obj1
        obj1.update(obj2)
        return obj1
    

    def Environment(self, name: str):
        ''' 👉️ Returns a configuration from os.environ, i.e. same as 'os.environ[name]'.'''
        import os
        return os.environ[name]
