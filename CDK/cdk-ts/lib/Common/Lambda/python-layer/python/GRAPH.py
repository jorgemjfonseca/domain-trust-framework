# 📚 Graph: https://quip.com/hgz4A3clvOes/-Graph

# TODO implement graph DB


def test():
    return 'this is SUBSCRIBER test.'


class GRAPH:
    

    @staticmethod
    def _getDomainItem(domainName):
        from DYNAMO import DYNAMO
        domains = DYNAMO('DOMAINS')
        domain = domains.Get(domainName)
        return domain


    @staticmethod
    def _getDomainItemManifest(domainName):

        item = GRAPH._getDomainItem(domainName)        

        from MANIFEST import MANIFEST
        raw = item['Manifest']
        manifest = MANIFEST(raw)
        # TODO: test if we need a UTILS.FromYaml/Json

        return manifest


    @staticmethod
    def _getCodeItem(code):
        from DYNAMO import DYNAMO
        codes = DYNAMO('CODES')
        item = codes.Get(code)
        return item


    @staticmethod
    def _HandleConsumer(event):
        ''' 👉 https://quip.com/hgz4A3clvOes#temp:C:bDAeaf662df90ec442284b7aaef9 '''

        print(f'{event}')

        from DYNAMO import DYNAMO
        for r in DYNAMO.Records(event):

            domainName = r['Domain']

            from DOMAIN import DOMAIN
            domain = DOMAIN(domainName)
            manifest = domain.GetManifest()

            from UTILS import UTILS
            timestamp = UTILS.Timestamp()

            domains = DYNAMO('DOMAINS')
            domains.Merge(domainName, {
                'Domain': domainName,
                'Timestamp': timestamp,
                'Manifest': manifest
            })
            

    @staticmethod
    def _trusts(source, target, role, code):

        domain = GRAPH._getDomainItemManifest(source)
        if not domain:
            return False

        trust = domain.Trusts(
            domain=target, 
            role=role, 
            code=code)
        
        return trust

    
    @staticmethod
    def _HandleTrusted(event):
        ''' 👉 https://quip.com/hgz4A3clvOes/-Graph#temp:C:bDA0807933d618043e6b1873dc74 '''
        # TODO implement graph DB

        '''
        "Body": {
            "Domain": "ec.europa.eu",
            "Context": "VAULT",
            "Code": "iata.org/SSR/WCHR"
        }
        '''
        print(f'{event}')

        from MSG import MSG
        msg = MSG(event)

        source = msg.From()
        target = msg.TryAtt('Domain')
        role = msg.TryAtt('Role')
        code = msg.TryAtt('Code')

        trust = GRAPH._trusts(source, target, role, code)

        return {
            'Trusted': trust,
            'Important': 'Chained trust not yet implemented.'
        }
    
    
    @staticmethod
    def _HandleTrusts(event):
        ''' 👉 https://quip.com/hgz4A3clvOes#temp:C:bDA71b470c7a4c446e5b43adea7e '''
        # TODO implement graph DB

        '''
        "Body": {
            "Truster": "heathrow.com",
            "Trusted": "airfrance.fr",    
            "Context": "CONSUMER",
            "Code": "dtfw.org/PALM/FOUND"
        }
        '''
        
        print(f'{event}')
        
        from MSG import MSG
        msg = MSG(event)

        source = msg.TryAtt('Truster')
        target = msg.TryAtt('Domain')
        role = msg.TryAtt('Role')
        code = msg.TryAtt('Code')

        trust = GRAPH._trusts(source, target, role, code)

        return {
            'Trusted': trust,
            'Important': 'Chained trust not yet implemented.'
        }
    

    @staticmethod
    def _HandleIdentity(event):
        ''' 👉 https://quip.com/hgz4A3clvOes#temp:C:bDAacb56742c6a342a8a3494587d '''

        '''
        "Body": {
            "Domain": "example.com"
        }
        '''
        print(f'{event}')

        from MSG import MSG
        msg = MSG(event)
        domainName = msg.TryAtt('Domain')

        domain = GRAPH._getDomainItemManifest(domainName)
        identity = domain.Identity()
        return identity
    

    @staticmethod
    def _HandleQueryable(event):
        ''' 👉 https://quip.com/hgz4A3clvOes#temp:C:bDA44399e7e0bfc4609a560d6c4a '''
        # TODO: implement the logic

        '''
        "Body": {
            "Host": "any-host.com",
            "Binds": [{
                "Vault": "ec.europa.eu",
                    "Code": "iata.org/SSR/WCHR"
            }]
        }
        '''
        print(f'{event}')
        
        from MSG import MSG
        msg = MSG(event)
        binds = msg.TryAtt('Binds')
        
        binds['Alert'] = 'Logic not yet implemented, this is just an echo!'
        return binds
    

    @staticmethod
    def _HandleTranslate(event):
        ''' 👉 https://quip.com/hgz4A3clvOes#temp:C:bDA9d34010d13574c2f95fe4de54 '''

        '''
        "Body": {
            "Language": "pt-br",
            "Domains": ["example.com"],
            "Codes": ["iata.org/SSR/WCHR"]
        }
        '''
        print(f'{event}')

        ret = {
            "Language": language,
            "Domains": [],
            "Codes": []
        }

        from MSG import MSG
        msg = MSG(event)

        language = msg.TryAtt('Language')
        domains = msg.TryAtt('Domains', default=[])
        codes = msg.TryAtt('Codes', default=[])

        if not language:
            return ret
        
        for domain in domains:
            manifest = GRAPH._getDomainItemManifest(domain)
            translation = manifest.NameTranslation(language)
            ret['Domains'].append({
                'Domain': domain,
                'Translation': translation
            })

        from MANIFEST import MANIFEST
        for code in codes:
            item = GRAPH._getCodeItem(code)
            translation = MANIFEST.CodeTranslation(item, language)
            ret['Codes'].append({
                'Code': code,
                'Translation': translation
            })
        
        return ret
    

    @staticmethod
    def _HandlePublicKey(event):
        ''' 👉 https://quip.com/hgz4A3clvOes#temp:C:bDAe17e4b66e30846a7b82ecce0c '''
        # TODO: implement when there's an old issuer who has rotated their keys.

        '''
        "Body": {
            "Issuer": "nhs.uk",
            "Date": "2022/01/09"
        }
        '''

        print(f'{event}')
        return {
            'Alert': 'Not yet implemented!'
        }
    

    @staticmethod
    def _HandleSchema(event):
        ''' 👉 https://quip.com/hgz4A3clvOes#temp:C:bDAe24fd83cf9c244078a0f67f7f '''

        '''
        "Body": {
            "Code": "iata.org/SSR/WCHR",
            "Output": "QR",
            "Version": "A"
        }
        '''
        print(f'{event}')

        from MSG import MSG
        msg = MSG(event)

        code = msg.TryAtt('Code')
        output = msg.TryAtt('Output')
        version = msg.TryAtt('Version')

        item = GRAPH._getCodeItem(code)

        from MANIFEST import MANIFEST
        schema = MANIFEST.CodeSchema(item=item, output=output, version=version)

        return schema
    

    @staticmethod
    def _HandlePublisher(event):
        
        from MSG import MSG
        msg = MSG(event)
        domainName = msg.From()
        
        from MANIFEST import MANIFEST
        manifest = MANIFEST()
        manifest.LoadFromDomain(domainName)        

        from DYNAMO import DYNAMO
        domains = DYNAMO('DOMAINS')
        codes = DYNAMO('CODES')

        # TODO: save the domain and code
        # TODO: Ignore older records by looking at the Timestamps (envelope+table)
        # TODO: Ignore codes that don't match the domain
        # TODO: Handle codes that are delegate to other domains

        print(f'{event}')
        return {}