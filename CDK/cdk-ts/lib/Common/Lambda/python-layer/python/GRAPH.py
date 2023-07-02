# 📚 Graph: https://quip.com/hgz4A3clvOes/-Graph

# TODO implement graph DB


def test():
    return 'this is SUBSCRIBER test.'


class GRAPH:
    

    @staticmethod
    def _HandleConsumer(event):
        ''' 👉 https://quip.com/hgz4A3clvOes#temp:C:bDAeaf662df90ec442284b7aaef9 '''

        print(f'{event}')

        from DYNAMO import DYNAMO
        for r in DYNAMO.Records(event):

            domainName = r['Domain']
            
            from DOMAIN import DOMAIN
            domain = DOMAIN(domainName)
            yaml = domain.GetManifest()

            from UTILS import UTILS
            timestamp = UTILS.Timestamp()
            manifest = UTILS.FromYaml(yaml)

            domains = DYNAMO('DOMAINS')
            domains.Merge(domainName, {
                'Domain': domainName,
                'Timestamp': timestamp,
                'Manifest': manifest
            })
            
    
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

        domainName = msg.TryAtt('Domain')
        role = msg.TryAtt('Role')
        code = msg.TryAtt('Code')

        from MANIFEST import MANIFEST
        manifest = MANIFEST(yaml)
        trusted = MANIFEST.Trusts(
            domain=domainName, 
            role=role, 
            code=code)

        return {
            'Trusted': trusted,
            'Important': 'Not yet implemented, always returns True.'
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
        
        return {
            "Trusted": True,
            "Important": "Not yet implemented, always returns True."
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
        return {}
    

    @staticmethod
    def _HandleQueryable(event):
        ''' 👉 https://quip.com/hgz4A3clvOes#temp:C:bDA44399e7e0bfc4609a560d6c4a '''

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
        return {}
    

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
        return {}
    

    @staticmethod
    def _HandlePublicKey(event):
        ''' 👉 https://quip.com/hgz4A3clvOes#temp:C:bDAe17e4b66e30846a7b82ecce0c '''

        '''
        "Body": {
            "Issuer": "nhs.uk",
            "Date": "2022/01/09"
        }
        '''

        print(f'{event}')
        return {}
    

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
        return {}
    

    @staticmethod
    def _HandlePublisher(event):
        
        print(f'{event}')
        return {}