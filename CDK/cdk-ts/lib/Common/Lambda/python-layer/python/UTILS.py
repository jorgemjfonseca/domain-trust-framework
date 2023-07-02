# 📚 UTILS

import json

def test():
    return 'this is a UTILS test.'


class NotFoundException(Exception):
    pass

class InvalidRequestException(Exception):
    pass


class UTILS: 


    @staticmethod
    def RaiseNotFoundException():
        raise NotFoundException
    

    @staticmethod
    def RaiseInvalidRequestException():
        raise InvalidRequestException
    

    @staticmethod
    def FromJson(text: str) -> any:
        return json.loads(text)
        
    
    @staticmethod
    def ToJson(obj: any) -> str:
        return json.dumps(obj)
    
    
    @staticmethod
    def FromYaml(text: str) -> any:
        ''' 
        👉 https://yaml.readthedocs.io/en/latest/detail.html
        👉 https://stackoverflow.com/questions/50846431/converting-a-yaml-file-to-json-object-in-python
        👉 https://sourceforge.net/p/ruamel-yaml/code/ci/default/tree/
        👉 https://yaml.readthedocs.io/en/latest/
        👉 https://lyz-code.github.io/blue-book/coding/python/ruamel_yaml/
        '''

        # "products:\n  - item 1\n  - item 2\n"
        
        from ruamel.yaml import YAML
        from io import StringIO 
        
        yaml = YAML()
        stream = StringIO(text)
        data = yaml.load(stream)
        stream.close()
        
        return data
        
        
    @staticmethod
    def ToYaml(obj: any) -> str:
        ''' 👉 https://lyz-code.github.io/blue-book/coding/python/ruamel_yaml/ '''
        # {'products': ['item 1', 'item 2']}
        
        from ruamel.yaml import YAML
        from io import StringIO 
        
        # Configure YAML formatter
        yaml = YAML()
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.allow_duplicate_keys = True
        yaml.explicit_start = False
        
        # Return the output to a string
        stream = StringIO()
        yaml.dump(obj, stream)
        text = stream.getvalue()
        stream.close()
    
        return text


    @staticmethod
    def FromJsonToYaml(text: str) -> str:
        obj = UTILS.FromJson(text)
        return UTILS.ToYaml(obj)
        
        
    @staticmethod
    def FromYamlToJson(text: str) -> str:
        obj = UTILS.FromYaml(text)
        return UTILS.ToJson(obj)


    @staticmethod
    def Copy(obj):        
        from copy import deepcopy
        return deepcopy(obj)
    

    @staticmethod
    def UUID():
        ''' 👉️ https://stackoverflow.com/questions/37049289/how-do-i-convert-a-python-uuid-into-a-string '''
        import uuid
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
        import datetime
        timestamp = datetime.datetime.utcnow().isoformat() + 'Z'
        return timestamp


    @staticmethod
    def Canonicalize(object: any) -> str:
        ''' 👉️ https://bobbyhadz.com/blog/python-json-dumps-no-spaces '''
        import json
        canonicalized = json.dumps(object, separators=(',', ':'))
        print(f'{canonicalized=}')
        return canonicalized
    

    @staticmethod
    def HttpResponse(code=200, body='', format='json'):

        ret = {
            'statusCode': code,
        }

        if format == 'json':
            ret['body']: UTILS.ToJson(body)

        elif format == 'yaml':
            ret['body']: UTILS.ToYaml(body)
            # contentType: text/yaml -> shows on browser (because all text/* are text)
            # contentType: application/x-yaml -> downloads (or is it application/yaml?)
            ret["headers"] = {
                "content-type": 'text/yaml'
            }

        elif format == 'text':
            ret['body']: body

        else:
            ret['body']: body

        return ret

    
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