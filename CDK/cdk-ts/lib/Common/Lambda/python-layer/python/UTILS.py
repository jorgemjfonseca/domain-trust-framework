import json
import uuid
import datetime
from copy import deepcopy


def test():
    return 'this is a UTILS test.'


class UTILS: 


    @staticmethod
    def FromYaml(string: str) -> any:
        return {
            'Alert': 'UTILS.FromYaml is not yet implemented'
        }


    @staticmethod
    def Copy(obj):        
        return deepcopy(obj)
    

    @staticmethod
    def UUID():
        ''' 👉️ https://stackoverflow.com/questions/37049289/how-do-i-convert-a-python-uuid-into-a-string '''
        return str(uuid.uuid4());
    
    
    @staticmethod
    def Correlation():
        ''' 👉️ https://quip.com/NiUhAQKbj7zi#temp:C:XAYf6d35adc1f4e4f0795954ef86 '''
        correlation = UTILS.UUID();
        print(f'{correlation=}')
        return correlation


    @staticmethod
    def Timestamp():
        ''' 👉️ https://stackoverflow.com/questions/53676600/string-formatting-of-utcnow '''
        timestamp = datetime.datetime.utcnow().isoformat() + 'Z'
        return timestamp


    @staticmethod
    def Canonicalize(object: any) -> str:
        ''' 👉️ https://bobbyhadz.com/blog/python-json-dumps-no-spaces '''
        canonicalized = json.dumps(object, separators=(',', ':'))
        print(f'{canonicalized=}')
        return canonicalized
    

    @staticmethod
    def HttpResponse(code, body):
        return {
            'statusCode': code,
            'body': json.dumps(body)
        }

    
    @staticmethod
    def TryCall(obj, name):
        '''  👉️ https://bobbyhadz.com/blog/python-check-if-object-has-method#check-if-an-object-has-a-specific-method-in-python '''
        method = getattr(obj, name, None)
        if callable(method):
            return method()
        return obj


    @staticmethod
    def Merge(obj1, obj2):
        ''' 👉️ https://stackoverflow.com/questions/14839528/merge-two-objects-in-python '''
        obj1.update(obj2)
        return obj1