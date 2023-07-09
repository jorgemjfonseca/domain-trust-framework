# 📚 MANIFEST

# 👉 https://stackoverflow.com/questions/33533148/how-do-i-type-hint-a-method-with-the-type-of-the-enclosing-class
from __future__ import annotations

# 👉 https://stackoverflow.com/questions/24853923/type-hinting-a-collection-of-a-specified-type
from typing import List, Set, Tuple, Dict
from CODE import CODE


from DTFW import DTFW
from STRUCT import STRUCT
from UTILS import UTILS
dtfw = DTFW()

def test():
    return 'this is a MANIFEST test.'


class MANIFEST(STRUCT, DTFW, UTILS):
    ''' 📜 Wrapper of a YAML Manifest. '''
        

    def __init__(self, manifest: any = None, section:str=None):
        obj = manifest
        if manifest is MANIFEST:
            obj = manifest.Manifest()
        elif section != None: 
            obj = {}
            obj[section] = manifest
        else:
            obj = manifest
            
        super().__init__(obj=obj)



    def FromAppConfig(
        self, 
        CONFIG_APP: str = 'CONFIG_APP', 
        CONFIG_ENV: str = 'CONFIG_ENV', 
        CONFIG_PROFILE: str = 'CONFIG_PROFILE'
    ) -> any:
        ''' 
        👉 Reads the manifest's YAML from the AppConfig,
        then converts the YAML into an object, 
        then returns the object.
        '''
        
        yaml = dtfw.APPCONFIG().Get(CONFIG_APP, CONFIG_ENV, CONFIG_PROFILE)

        obj = self.UTILS().FromYaml(yaml)
        
        print (f'Manifest.FromAppConfig.return: {obj}')
        return obj
    
       
    def Fetch(self, domain) -> any:
        ''' Loads a manifest by reading the remote domain name. '''
        replace = self.DOMAIN(domain).FetchManifest()
        super().Obj(replace)


    def Trusts(self, domain, role, code) -> bool:
        ''' 📜 https://quip.com/lcSaAX7AiEXL#temp:C:RSEe24ce39a70604b598bebe8ff1 '''

        if domain == None or role == None or code == None:
            return False

        if self.IsMissingOrEmpty('Trust'):
            return False
        
        for trust in self.Structs('Trust'):

            # Discard on missing props, for safety of typos.
            if trust.IsMissingOrEmpty('Action'):
                return False
            if trust.IsMissingOrEmpty('Role'):
                return False
            if trust.IsMissingOrEmpty('Domains'):
                return False
            if trust.IsMissingOrEmpty('Queries'):
                return False

            # Discard on action mismatch.
            if trust.Att('Action') not in ['GRANT', '*']:
                continue

            # Discard on role mismatch.
            if trust.Att('Role') not in [role, '*']:
                continue
            
            # Discard on domain mismatch.
            domains = trust.Att('Domains')
            if [domain, '*'] not in domains:
                continue

            # Finally check for query match.
            queries = trust.Att('Queries')
            if [code, '*'] in queries:
                return True
                
            # Check if the query includes the code as *.
            for query in queries:
                if query.endswith('*'):
                    if code.startwith(query.replace('*', '')):
                        return True

        return False

    

    def Identity(self):
        return self.Att('Identity')
    

    def Domain(self):
        return self.Att(
            name= 'Domain',
            source= self.Identity(),
            default= '<MISSING>')
        

    def Name(self):
        return self.Att(
            name= 'Name', 
            source= self.Identity(), 
            default= self.Domain())


    def Translations(self, default=[]):
        return self.Att('Identity.Translations', default= default)
    

    def Translate(self, language):
        ''' 
        📜 Returns the translation of the domain title into a the given language. 
        👉 https://quip.com/lcSaAX7AiEXL/-Domain#temp:C:RSEbf2bcdeaf8e244ae885e09e41 
        '''
        translations = self.Translations(default=[])
        for translation in translations:
            if 'Language' in translation:
                if translation['Language'] == language:
                    return translation['Translation']
        return self.Name()
    

    def Codes(self) -> List[CODE]:
        '''
        📜 Returns the list of codes defined by the authority.
        👉 https://quip.com/3mKNASbBpnng#temp:C:eVd66f7803481a34db7a14b6698e
        '''
        ret = []
        for code in self.Structs('Codes'):
            ret.append(self.CODE(code))
        return ret
    

    def VerifyIdentity(self, expectedDomain:str):
        ''' 👉 Check if the manifest is valid for the given domain. '''
        id = self.RequireStruct('Identity')
        id.Match('Domain', expectedDomain)