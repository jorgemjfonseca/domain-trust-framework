def test():
    return 'this is a MANIFEST test.'


class MANIFEST:
        
    def __init__(self, manifest: any):
        self._manifest = manifest
    

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
    

    def FromDomain(domainName) -> any:
        from DOMAIN import DOMAIN
        domain = DOMAIN(domainName)
        return domain.GetManifest()


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