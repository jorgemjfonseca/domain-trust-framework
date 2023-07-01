# 📚 Graph: https://quip.com/hgz4A3clvOes/-Graph

# TODO implement graph DB

from UTILS import UTILS


def test():
    return 'this is SUBSCRIBER test.'


class GRAPH:
    

    @staticmethod
    def _HandleConsume(event):
        # 👉 https://quip.com/hgz4A3clvOes#temp:C:bDAeaf662df90ec442284b7aaef9

        '''
        "Body": {
            "Updates":[
                {
                    "UpdateID": "8e8cb55b-55a8-49a5-9f80-439138e340a2",
                    "Timestamp": "2018-12-10T13:45:00.000Z",
                    "Domain": "example.com",
                    "Correlation": "125a5c75-cb72-43d2-9695-37026dfcaa48"
                }
            ],
            "Token": "3b3615f2-c744-4113-bf4e-8252ad5cb548"
        }
        '''

        print(f'{event}')
        return {}
    

    @staticmethod
    def _HandleTrusted(event):
        # 👉 https://quip.com/hgz4A3clvOes/-Graph#temp:C:bDA0807933d618043e6b1873dc74
        # TODO implement graph DB

        '''
        "Body": {
            "Domain": "ec.europa.eu",
            "Context": "VAULT",
            "Code": "iata.org/SSR/WCHR"
        }
        '''

        print(f'{event}')

        return {
            "Trusted": True,
            "Important": "Not yet implemented, always returns true"
        }
    
    
    @staticmethod
    def _HandleTrusts(event):
        # 👉 https://quip.com/hgz4A3clvOes#temp:C:bDA71b470c7a4c446e5b43adea7e

        '''
        "Body": {
            "Truster": "heathrow.com",
            "Trusted": "airfrance.fr",    
            "Context": "CONSUMER",
            "Code": "dtfw.org/PALM/FOUND"
        }
        '''
        
        print(f'{event}')
        return {}
    

    @staticmethod
    def _HandleIdentity(event):
        # 👉 https://quip.com/hgz4A3clvOes#temp:C:bDAacb56742c6a342a8a3494587d

        '''
        "Body": {
            "Domain": "example.com"
        }
        '''
        
        print(f'{event}')
        return {}
    

    @staticmethod
    def _HandleQueryable(event):
        # 👉 https://quip.com/hgz4A3clvOes#temp:C:bDA44399e7e0bfc4609a560d6c4a

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
        # 👉 https://quip.com/hgz4A3clvOes#temp:C:bDA9d34010d13574c2f95fe4de54

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
        # 👉 https://quip.com/hgz4A3clvOes#temp:C:bDAe17e4b66e30846a7b82ecce0c

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
        # 👉 https://quip.com/hgz4A3clvOes#temp:C:bDAe24fd83cf9c244078a0f67f7f

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