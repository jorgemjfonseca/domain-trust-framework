# 📚 MANIFEST

from DTFW import DTFW
dtfw = DTFW()

def test():
    return 'this is a MANIFEST test.'


class MANIFEST:
        
    def __init__(self, manifest: any = None):
        if manifest is MANIFEST:
            self._manifest = manifest.Manifest()
        else:
            self._manifest = manifest
    

    def Manifest(self):
        return self._manifest


    def FromAppConfig(
        self, 
        CONFIG_APP: str = 'CONFIG_APP', 
        CONFIG_ENV: str = 'CONFIG_ENV', 
        CONFIG_PROFILE: str = 'CONFIG_PROFILE'
    ) -> any:
        
        yaml = dtfw.AppConfig().Get(CONFIG_APP, CONFIG_ENV, CONFIG_PROFILE)

        obj = dtfw.Utils().FromYaml(yaml)
        
        print (f'Manifest.FromAppConfig.return: {obj}')
        return obj
    

    def RawAppConfig(
        self, 
        CONFIG_APP: str = 'CONFIG_APP', 
        CONFIG_ENV: str = 'CONFIG_ENV', 
        CONFIG_PROFILE: str = 'CONFIG_PROFILE'
    ) -> str:
        
        from APPCONFIG import APPCONFIG
        yaml = APPCONFIG.Get(CONFIG_APP, CONFIG_ENV, CONFIG_PROFILE)

        return yaml
    

    def LoadFromAppConfig(
        self,
        CONFIG_APP: str = 'CONFIG_APP', 
        CONFIG_ENV: str = 'CONFIG_ENV', 
        CONFIG_PROFILE: str = 'CONFIG_PROFILE'
    ):
        self._manifestManifest.FromAppConfig(
            CONFIG_APP, CONFIG_ENV, CONFIG_PROFILE
        )
        

    def _fromDomain(self, domain) -> any:
        return dtfw.DOMAIN(domain).GetManifest()


    def Fetch(self, domain) -> any:
        ''' Loads a manifest by reading the remote domain name. '''
        self._manifest = self._fromDomain(domain)


    def Trusts(self, domain, role, code) -> bool:

        if domain == None or role == None or code == None:
            return False

        if 'Trust' not in self._manifest:
            return False
        trusts = self._manifest['Trust']
        
        for trust in trusts:

            # Discard on missing props, for safety of typos.
            if 'Action' not in trust:
                return False
            if 'Role' not in trust:
                return False
            if 'Domains' not in trust:
                return False
            if 'Queries' not in trust:
                return False

            # Discard on action mismatch.
            if trust['Action'] not in ['GRANT', '*']:
                continue

            # Discard on role mismatch.
            if trust['Role'] not in [role, '*']:
                continue
            
            # Discard on domain mismatch.
            domains = trust['Domains']
            if [domain, '*'] not in domains:
                continue

            # Finally check for query match.
            queries = trust['Queries']
            if [code, '*'] in queries:
                return True
                
            # Check if the query includes the code as *.
            for query in queries:
                if query.endswith('*'):
                    if code.startwith(query.replace('*', '')):
                        return True

        return False
    

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
        return MANIFEST._att(name, source, default)
    

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
        return self.Att(
            name= 'Translations',
            source= self.Identity(),
            default= default)
    

    def Translate(self, language):
        translations = self.Translations(default=[])
        for translation in translations:
            if 'Language' in translation:
                if translation['Language'] == language:
                    return translation['Translation']
        return self.Name()