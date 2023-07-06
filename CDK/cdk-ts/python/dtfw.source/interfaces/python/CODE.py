# 📚 CODE

from ITEM import ITEM
from STRUCT import STRUCT


class CODE(ITEM):
    

    def Schema(self, output:str, version:str=None):
        for schema in self.Structs('Schemas'):
            if schema.Att('Output') == output:
                if version == None: 
                    return schema
                if schema.IsMissingOrEmpty('Version'):
                    return schema
                if schema.Att('Output') == version:
                    return schema
        return STRUCT({})
    

    def Translate(self, language:str) -> str:
        translations = self.Structs('Translations')
        for translation in translations:
            if translation.Att('Language') == language:
                return translation.Att('Translation')
        return self.ID()