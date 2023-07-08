# 📚 YAML

import json

from STRUCT import STRUCT


class YAML: 


    def FromJson(self, text: str):
        return STRUCT(json.loads(text))
        
    
    def ToJson(self, obj: any):
        ''' 👉 Converts the object into a json string.'''
        print(f'YAML.ToJson: {obj=}')
        return json.dumps(obj)
    
    
    def FromYaml(self, text: str) -> any:
        print(f'YAML.FromYaml: {text=}')
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