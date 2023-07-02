def test():
    return 'this is a MANIFEST test.'


import MANIFEST as MANIFEST

class MANIFEST:
        
    def __init__(self, manifest: any = None):
        if manifest is MANIFEST:
            self._manifest = manifest.Manifest()
        else:
            self._manifest = manifest
    

    def Manifest(self):
        return self._manifest


    @staticmethod
    def FromAppConfig(
        CONFIG_APP: str = 'CONFIG_APP', 
        CONFIG_ENV: str = 'CONFIG_ENV', 
        CONFIG_PROFILE: str = 'CONFIG_PROFILE'
    ) -> any:
        
        from APPCONFIG import APPCONFIG
        yaml = APPCONFIG.Get(CONFIG_APP, CONFIG_ENV, CONFIG_PROFILE)

        from UTILS import UTILS
        obj = UTILS.FromYaml(yaml)

        return obj
    

    @staticmethod
    def RawAppConfig(
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
        self._manifest = MANIFEST.FromAppConfig(
            CONFIG_APP, CONFIG_ENV, CONFIG_PROFILE
        )
        

    @staticmethod
    def FromDomain(domainName) -> any:
        from DOMAIN import DOMAIN
        domain = DOMAIN(domainName)
        return domain.GetManifest()


    def LoadFromDomain(self, domainName) -> any:
        self._manifest = MANIFEST.FromDomain(domainName)


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
    def _tryAtt(name:str, source:any, default=None) -> any:
        ''' Returns a copy of the attribute, or [default] of it doesnt exist. '''
        if name in source:
            return source[name]
        return default


    def TryAtt(self, name:str, source:any=None, default=None) -> any:
        ''' Returns a copy of the attribute, or [default] of it doesnt exist. '''
        if not source:
            source = self._manifest
        return MANIFEST._tryAtt(name, source, default)
    

    def Identity(self):
        return self.TryAtt('Identity')
    

    def Domain(self):
        return self.TryAtt(
            name= 'Domain',
            source= self.Identity(),
            default= '<MISSING>')
        

    def Name(self):
        return self.TryAtt(
            name= 'Name', 
            source= self.Identity(), 
            default= self.Domain())


    def Translations(self, default=[]):
        return self.TryAtt(
            name= 'Translations',
            source= self.Identity(),
            default= default)
    

    def NameTranslation(self, language):
        translations = self.Translations(default=[])
        for translation in translations:
            if 'Language' in translation:
                if translation['Language'] == language:
                    return translation['Translation']
        return self.Name()
    

    @staticmethod
    def CodeTranslation(item, language):
        translations = MANIFEST._tryAtt('Translations', source=item, default=[])
        for translation in translations:
            if 'Language' in translation:
                if translation['Language'] == language:
                    return translation['Translation']
        return item['ID']
    

    @staticmethod
    def CodeSchema(item, output, version):
        if not item:
            return {}

        schemas = MANIFEST._tryAtt('Schemas', source=item, default=[])
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