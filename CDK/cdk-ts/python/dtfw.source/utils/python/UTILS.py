# 📚 UTILS

import json

def test():
    return 'this is a UTILS test.'


class NotFoundException(Exception):
    pass

class InvalidRequestException(Exception):
    pass


class UTILS: 


    def Struct(self, obj):
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
    

    def FromJson(self, text: str):
        return self.Struct(json.loads(text))
        
    
    def ToJson(self, obj: any):
        ''' 👉 Converts the object into a json string.'''
        print(f'Utils.ToJson: {obj=}')
        return json.dumps(obj)
    
    
    def FromYaml(self, text: str) -> any:
        print(f'Utils.FromYaml: {text=}')
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
        
        
    def ToYaml(self, obj: any) -> str:
        ''' 👉 https://lyz-code.github.io/blue-book/coding/python/ruamel_yaml/ '''
        # {'products': ['item 1', 'item 2']}
        
        from STRUCT import STRUCT
        data = obj
        if isinstance(obj, STRUCT):
            data = obj.Obj()

        from ruamel.yaml import YAML
        from io import StringIO 
        
        # Configure YAML formatter
        yaml = YAML()
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.allow_duplicate_keys = True
        yaml.explicit_start = False
        
        # Return the output to a string
        stream = StringIO()
        yaml.dump(data, stream)
        text = stream.getvalue()
        stream.close()
    
        return text


    def FromJsonToYaml(self, text: str) -> str:
        obj = self.FromJson(text)
        return self.ToYaml(obj)
        
        
    def FromYamlToJson(self, text: str) -> str:
        obj = self.FromYaml(text)
        return self.ToJson(obj)


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
        ''' 👉️ https://stackoverflow.com/questions/53676600/string-formatting-of-utcnow '''
        import datetime
        timestamp = datetime.datetime.utcnow().isoformat() + 'Z'
        return timestamp


    def Canonicalize(self, object: any) -> str:
        ''' 👉️ https://bobbyhadz.com/blog/python-json-dumps-no-spaces '''
        import json
        canonicalized = json.dumps(object, separators=(',', ':'))
        print(f'{canonicalized=}')
        return canonicalized
    

    def HttpResponse(self, code=200, body='', format='json'):
        print(f'HttpResponse: {body=}')
        print(f'HttpResponse: {format=}')

        ret = {
            'statusCode': code,
        }

        if format == 'json':
            ret['body'] = self.ToJson(body)

        elif format == 'yaml':
            ret['body'] = self.ToYaml(body)
            # contentType: text/yaml -> shows on browser (because all text/* are text)
            # contentType: application/x-yaml -> downloads (or is it application/yaml?)
            ret["headers"] = {
                "content-type": 'application/x-yaml'
            }

        elif format == 'text':
            ret['body'] = body

        else:
            ret['body'] = body

        print(f'HttpResponse: {ret=}')
        return ret

    
    def TryCall(self, obj, name):
        '''  👉️ https://bobbyhadz.com/blog/python-check-if-object-has-method#check-if-an-object-has-a-specific-method-in-python '''
        method = getattr(obj, name, None)
        if callable(method):
            return method()
        return obj


    def Merge(self, obj1, obj2):
        ''' 👉️ https://stackoverflow.com/questions/14839528/merge-two-objects-in-python '''
        obj1.update(obj2)
        return obj1