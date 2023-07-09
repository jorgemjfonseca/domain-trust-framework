# 📚 CODE

from ITEM import ITEM
from STRUCT import STRUCT


class CODE(ITEM):
    ''' 📜 https://quip.com/3mKNASbBpnng#temp:C:eVd92c29500621a4395928f6d216 '''


    def Schema(self, output:str, version:str=None):
        ''' 📜 https://quip.com/3mKNASbBpnng#temp:C:eVd9964011c8a8c43a495f1eca5c '''
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
        ''' 📜 https://quip.com/3mKNASbBpnng#temp:C:eVd66f7803481a34db7a14b6698e '''
        translations = self.Structs('Translations')

        for translation in translations:
            if translation.Att('Language') == language:
                return translation.Att('Translation')
            
        return self.ID()