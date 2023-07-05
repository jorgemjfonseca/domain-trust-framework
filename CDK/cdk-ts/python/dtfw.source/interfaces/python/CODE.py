# 📚 CODE

from DTFW import DTFW
dtfw = DTFW()


def test():
    return 'this is a CODE test.'


class CODE:
        
    def __init__(self, item):
        self._item = item
    

    def Item(self):
        return self._item


    @staticmethod
    def _att(name:str, source:any, default=None) -> any:
        ''' Returns a copy of the attribute, or [default] of it doesnt exist. '''
        if name in source:
            return source[name]
        return default


    def Att(self, name:str, source:any=None, default=None) -> any:
        ''' Returns a copy of the attribute, or [default] of it doesnt exist. '''
        if not source:
            source = self._manifest
        return CODE._att(name, source, default)
    

    def Schema(self, output, version):
        if not self._item:
            return {}

        schemas = self.Att('Schemas', default=[])
        for schema in schemas:
            if 'Output' in schema:
                if schema['Output'] == output:
                    if not version: 
                        return schema
                    if 'Version' not in schema:
                        return schema
                    if version == schema['Output']:
                        return schema
        return {}  
    

    def Translate(self, language):
        translations = self.Att('Translations', default=[])
        for translation in translations:
            if 'Language' in translation:
                if translation['Language'] == language:
                    return translation['Translation']
        return self.Att('ID')