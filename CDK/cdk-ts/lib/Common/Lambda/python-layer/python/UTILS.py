import json
import uuid
import datetime



def test():
    return 'this is a UTILS test.'


class UTILS: 

    # 👉️ https://stackoverflow.com/questions/37049289/how-do-i-convert-a-python-uuid-into-a-string
    @staticmethod
    def Correlation():
        correlation = str(uuid.uuid4());
        print(f'{correlation=}')
        return correlation


    # 👉️ https://stackoverflow.com/questions/53676600/string-formatting-of-utcnow
    @staticmethod
    def Timestamp():
        timestamp = datetime.datetime.utcnow().isoformat() + 'Z'
        return timestamp


    # 👉️ https://bobbyhadz.com/blog/python-json-dumps-no-spaces
    @staticmethod
    def Canonicalize(object: any) -> str:
        canonicalized = json.dumps(object, separators=(',', ':'))
        print(f'{canonicalized=}')
        return canonicalized
    

    @staticmethod
    def HttpResponse(code, body):
        return {
            'statusCode': code,
            'body': json.dumps(body)
        }


    # 👉️ https://bobbyhadz.com/blog/python-check-if-object-has-method#check-if-an-object-has-a-specific-method-in-python
    @staticmethod
    def TryCall(obj, name):
        method = getattr(obj, name, None)
        if callable(method):
            return method()
        return obj


    # 👉️ https://stackoverflow.com/questions/14839528/merge-two-objects-in-python
    @staticmethod
    def Merge(obj1, obj2):
        obj1.update(obj2)
        return obj1