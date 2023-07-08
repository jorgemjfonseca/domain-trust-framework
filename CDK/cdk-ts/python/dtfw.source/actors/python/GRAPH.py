# 📚 GRAPH: https://quip.com/hgz4A3clvOes/-Graph

# TODO implement graph DB


from DYNAMO import DYNAMO
from MSG import MSG
from STRUCT import ITEM, STRUCT
from DTFW import DTFW


class GRAPH(DTFW):
    
    
    def _graphDomain(self) -> str: 
        # TODO implement discovery on the client side
        return '<TBD GRAPH>'
    

    def _trusts(self, source, target, role, code):
        ''' 🏃 Internal method to search a trust path in the database. '''
        # TODO implement graph DB

        domain = self.MANIFEST(source)
        if not domain:
            return False

        return domain.Trusts(
            domain=target, 
            role=role, 
            code=code)
    


    def HandleQueryable(self, event):
        ''' 🚀 https://quip.com/hgz4A3clvOes#temp:C:bDA44399e7e0bfc4609a560d6c4a '''
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
        
        binds = self.MSG(event).Att('Binds')
        binds['Alert'] = 'Logic not yet implemented, this is just an echo!'
        return binds
    

    def HandlePublicKey(self, event):
        ''' 🚀 https://quip.com/hgz4A3clvOes#temp:C:bDAe17e4b66e30846a7b82ecce0c '''
        # TODO: implement when there's an old issuer who has rotated their keys.

        '''
        "Body": {
            "Issuer": "nhs.uk",
            "Date": "2022/01/09"
        }
        '''
        msg = self.MSG(event)
        return {
            'Alert': 'Not yet implemented!'
        }
    


    # ✅ DONE
    def Domains(self):
        return self.DYNAMO('DOMAINS')
    
    
    # ✅ DONE
    def LoadManifest(self, domain):
        item = self.Domains().Get(domain)
        yaml = item.Require('Manifest')
        obj = self.FromYaml(yaml)
        manifest = self.MANIFEST(obj)
        return manifest


    # ✅ DONE
    def Codes(self) -> DYNAMO:
        return self.DYNAMO('CODES')
    

    # ✅ DONE
    def LoadCode(self, code):
        item = self.Codes().Get(code)
        struct = self.CODE(item)
        return struct


    # ✅ DONE
    def Invoke(self, subject, body: any) -> STRUCT: 
        ''' 👉 Sends a message to the registered Graph endpoint. '''
        resp = self.SyncApi().Send(
            to= self._graphDomain(),
            subject= subject,
            body= body)
        return self.STRUCT(resp)


    # ✅ DONE
    def HandleSubscriber(self, event):
        ''' 🐌 https://quip.com/hgz4A3clvOes#temp:C:bDAeaf662df90ec442284b7aaef9 '''

        print(f'{event}')

        for r in self.DYNAMO().Records(event):

            domainName = r['Domain']

            self.Domains().Upsert(domainName, {
                'Domain': domainName,
                'Timestamp': self.Timestamp(),
                'Manifest': self.DOMAIN(domainName).FetchManifest()
            })
        

    # ✅ DONE
    def InvokeTrusted(self, domain, context, code) -> bool: 
        ''' 🏃 https://quip.com/hgz4A3clvOes/-Graph#temp:C:bDA0807933d618043e6b1873dc74 '''
        '''
        "Body": {
            "Domain": "ec.europa.eu",
            "Context": "VAULT",
            "Code": "iata.org/SSR/WCHR"
        }
        '''
        resp = self.Invoke(
            subject= 'Trusted@Graph', 
            body={
                "Domain": domain,
                "Context": context,
                "Code": code
            })

        return resp.RequireBool('Trusted')

    
    # ✅ DONE
    def HandleTrusted(self, event):
        ''' 🚀 https://quip.com/hgz4A3clvOes/-Graph#temp:C:bDA0807933d618043e6b1873dc74 '''
        

        '''
        "Body": {
            "Domain": "ec.europa.eu",
            "Context": "VAULT",
            "Code": "iata.org/SSR/WCHR"
        }
        '''
        msg = self.MSG(event)

        trusts = self._trusts(
            source= msg.From(),
            target= msg.Require('Domain'), 
            role= msg.Att('Role'), 
            code= msg.Att('Code'))

        return {
            'Trusted': trusts,
            'Important': 'Chained trust not yet implemented.'
        }
    
    
    # ✅ DONE
    def HandleTrusts(self, event):
        ''' 🚀 https://quip.com/hgz4A3clvOes#temp:C:bDA71b470c7a4c446e5b43adea7e '''
        
        '''
        "Body": {
            "Truster": "heathrow.com",
            "Trusted": "airfrance.fr",    
            "Context": "CONSUMER",
            "Code": "dtfw.org/PALM/FOUND"
        }
        '''
        msg = self.MSG(event)

        source = msg.Require('Truster')
        target = msg.Require('Domain')
        role = msg.Att('Role')
        code = msg.Att('Code')

        trust = self._trusts(source, target, role, code)

        return {
            'Trusted': trust
        }
    

    # ✅ DONE
    def HandleIdentity(self, event):
        ''' 🚀 https://quip.com/hgz4A3clvOes#temp:C:bDAacb56742c6a342a8a3494587d '''

        '''
        "Body": {
            "Domain": "example.com"
        }
        '''
        domainName = self.MSG(event).Att('Domain')
        return self.MANIFEST(domainName).Identity()
    

    # ✅ DONE
    def InvokeTranslate(self, body: any) -> STRUCT: 
        ''' 🏃 https://quip.com/hgz4A3clvOes#temp:C:bDA9d34010d13574c2f95fe4de54 '''
        return self.Invoke(
            subject='Translate@Graph', 
            body=body)
    

    # ✅ DONE
    def HandleTranslate(self, event):
        ''' 🚀 https://quip.com/hgz4A3clvOes#temp:C:bDA9d34010d13574c2f95fe4de54 '''

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

        msg = self.MSG(event)

        language = msg.Att('Language')
        domains = msg.Att('Domains', default=[])
        codes = msg.Att('Codes', default=[])

        if not language:
            return ret
        
        for domain in domains:
            translation = self.LoadManifest(domain).Translate(language)
            ret['Domains'].append({
                'Domain': domain,
                'Translation': translation
            })

        for code in codes:
            translation = self.LoadCode(code).Translate(language)
            ret['Codes'].append({
                'Code': code,
                'Translation': translation
            })
        
        '''
        {
            "Language": "pt-br",
            "Domains": [{
                "Domain": "example.com",
                "Translation": "Example Airlines"
            }],
            "Codes": [{
                "Code": "iata.org/SSR/WCHR",
                "Translation": "Wheelchair assistance required"
            }]
        }
        '''

        return ret
    

    # ✅ DONE
    def HandleSchema(self, event):
        ''' 🚀 https://quip.com/hgz4A3clvOes#temp:C:bDAe24fd83cf9c244078a0f67f7f '''

        '''
        "Body": {
            "Code": "iata.org/SSR/WCHR",
            "Output": "QR",
            "Version": "A"
        }
        '''
        msg = self.MSG(event)
        code = msg.Att('Code')

        return self.LoadCode(code).Schema(
            output= msg.Att('Output'), 
            version= msg.Att('Version'))
