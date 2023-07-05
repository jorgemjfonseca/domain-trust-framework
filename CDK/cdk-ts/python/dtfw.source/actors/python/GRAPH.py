# 📚 GRAPH: https://quip.com/hgz4A3clvOes/-Graph

# TODO implement graph DB


def test():
    return 'this is SUBSCRIBER test.'


from DYNAMO import DYNAMO
from DTFW import DTFW

dtfw = DTFW()

class GRAPH:
    

    def Domains(self) -> DYNAMO:
        return dtfw.Dynamo('DOMAINS')
    def Domain(self, domainName):
        return self.Domains().Get(domainName)


    def Manifest(self, domainName):
        item = self.Domain(domainName)        
        manifest = dtfw.Manifest(item['Manifest'])
        # TODO: test if we need a UTILS.FromYaml/Json

        return manifest


    def Codes(self) -> DYNAMO:
        return dtfw.Dynamo('CODES')
    def Code(self, code):
        return self.Codes().Get(code)


    def HandleConsumer(self, event):
        ''' 👉 https://quip.com/hgz4A3clvOes#temp:C:bDAeaf662df90ec442284b7aaef9 '''

        print(f'{event}')

        for r in dtfw.Dynamo().Records(event):

            domainName = r['Domain']

            dtfw.Dynamo('DOMAINS').Merge(domainName, {
                'Domain': domainName,
                'Timestamp': dtfw.Utils().Timestamp(),
                'Manifest': dtfw.Domain(domainName).Manifest()
            })
            

    def _trusts(self, source, target, role, code):
        domain = self.Manifest(source)
        if not domain:
            return False

        return domain.Trusts(
            domain=target, 
            role=role, 
            code=code)
        

    def InvokeTrusted(self, domain, context, code) -> bool: 
        ''' 👉 https://quip.com/hgz4A3clvOes/-Graph#temp:C:bDA0807933d618043e6b1873dc74 '''
        '''
        "Body": {
            "Domain": "ec.europa.eu",
            "Context": "VAULT",
            "Code": "iata.org/SSR/WCHR"
        }
        '''
        
        msg = dtfw.Msg()

        # TODO implement discovery on the client side
        msg.To('<TBD GRAPH>')

        msg.Body({
            "Domain": domain,
            "Context": context,
            "Code": code
        })

        resp = dtfw.SyncApi().Send(msg)

        return dtfw.Item(resp).Require('Trusted')

    
    def HandleTrusted(self, event):
        ''' 👉 https://quip.com/hgz4A3clvOes/-Graph#temp:C:bDA0807933d618043e6b1873dc74 '''
        # TODO implement graph DB

        '''
        "Body": {
            "Domain": "ec.europa.eu",
            "Context": "VAULT",
            "Code": "iata.org/SSR/WCHR"
        }
        '''
        msg = dtfw.Msg(event)

        trusts = self._trusts(
            source= msg.From(),
            target= msg.Att('Domain'), 
            role= msg.Att('Role'), 
            code= msg.Att('Code'))

        return {
            'Trusted': trusts,
            'Important': 'Chained trust not yet implemented.'
        }
    
    
    def HandleTrusts(self, event):
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
        msg = dtfw.Msg(event)

        source = msg.Att('Truster')
        target = msg.Att('Domain')
        role = msg.Att('Role')
        code = msg.Att('Code')

        trust = self._trusts(source, target, role, code)

        return {
            'Trusted': trust,
            'Important': 'Chained trust not yet implemented.'
        }
    

    def HandleIdentity(self, event):
        ''' 👉 https://quip.com/hgz4A3clvOes#temp:C:bDAacb56742c6a342a8a3494587d '''

        '''
        "Body": {
            "Domain": "example.com"
        }
        '''
        domainName = dtfw.Msg(event).Att('Domain')
        return self.Manifest(domainName).Identity()
    

    def HandleQueryable(self, event):
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
        
        binds = dtfw.Msg(event).Att('Binds')
        binds['Alert'] = 'Logic not yet implemented, this is just an echo!'
        return binds
    

    def HandleTranslate(self, event):
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

        msg = dtfw.Msg(event)

        language = msg.Att('Language')
        domains = msg.Att('Domains', default=[])
        codes = msg.Att('Codes', default=[])

        if not language:
            return ret
        
        for domain in domains:
            translation = self.Manifest(domain).Translate(language)
            ret['Domains'].append({
                'Domain': domain,
                'Translation': translation
            })

        for code in codes:
            item = self.Code(code)
            translation = dtfw.Code(item).Translate(language)
            ret['Codes'].append({
                'Code': code,
                'Translation': translation
            })
        
        return ret
    

    def HandlePublicKey(self, event):
        ''' 👉 https://quip.com/hgz4A3clvOes#temp:C:bDAe17e4b66e30846a7b82ecce0c '''
        # TODO: implement when there's an old issuer who has rotated their keys.

        '''
        "Body": {
            "Issuer": "nhs.uk",
            "Date": "2022/01/09"
        }
        '''
        msg = dtfw.Msg(event)
        return {
            'Alert': 'Not yet implemented!'
        }
    

    def HandleSchema(self, event):
        ''' 👉 https://quip.com/hgz4A3clvOes#temp:C:bDAe24fd83cf9c244078a0f67f7f '''

        '''
        "Body": {
            "Code": "iata.org/SSR/WCHR",
            "Output": "QR",
            "Version": "A"
        }
        '''
        msg = dtfw.Msg(event)
        code = msg.Att('Code')
        item = self.Code(code)

        return dtfw.Code(item).Schema(
            output= msg.Att('Output'), 
            version= msg.Att('Version'))
    

    def HandlePublisher(self, event):
        
        domainName = dtfw.Msg(event).From()
        manifest = dtfw.Manifest().Fetch(domainName)

        # TODO: save the domain and code
        # TODO: Ignore older records by looking at the Timestamps (envelope+table)
        # TODO: Ignore codes that don't match the domain
        # TODO: Handle codes that are delegate to other domains

        print(f'{event}')
        return {}