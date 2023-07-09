# 📚 WALLET

def test():
    return 'this is WALLET test.'

# 👉 https://stackoverflow.com/questions/24853923/type-hinting-a-collection-of-a-specified-type
from typing import List, Set, Tuple, Dict

from ITEM import ITEM
from STRUCT import STRUCT
from MSG import MSG
from DTFW import DTFW

dtfw = DTFW()


class WALLET(ITEM):
    ''' 🪣 https://quip.com/zaYoA4kibXAP/-Broker-Setup#temp:C:DQN5a1b1a16ec7f4a29907cd1215
    {    
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "WalletQR": "🤝dtfw.org/WALLET,1,any-trust-broker.com,1AB2CD",
            "WalletQRURL": "https://any.broker.com/tf/qr/1AB2CD",
            "Language": "en-us",
            "Locator": "1AB2CD",
            "PublicKey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDH+wPrKYG1KVlzQUVtBghR8n9dzcShSZo0+3KgyVdOea7Ei7vQ1U4wRn1zlI5rSqHDzFitblmqnB2anzVvdQxLQ3UqEBKBfMihnLgCSW8Xf7MCH+DSGHNvBg2xSNhcfEmnbLPLnbuz4ySn1UB0lH2eqxy50zstxhTY0binD9Y+rwIDAQAB",
            "Notifier": "any-wallet.com",
            "Hosts": [{
                "Host": "iata.org",
                "Translation": "IATA",
                "Language": "en-us",
                "Sessions": [{
                    "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",
                    "SessionTime": "2018-12-10T13:45:00.000Z"
                }]
            }],
            "Vaults": [{
                "Vault": "iata.org",
                "Translation": "IATA",
                "Binds": [{
                    "BindID": "793af21d-12b1-4cea-8b55-623a19a28fc5",
                    "Code": "iata.org/SSR/WCHR",
                    "Translation": "Wheelchair for ramp"
                }]
            }],
            "Issuers": {
                "Issuer": "nhs.uk",
                "Translation": "NHS",
                "Credentials": [{
                    "CredentialID": "7bcf138b-db79-4a42-9d36-2655f8ff1f7c",
                    "Code": "iata.org/SSR/WCHR",
                    "Translation": "Wheelchair for ramp"
                    "Path": "/storage/tf/creds/nhs.uk/7bcf138b-db79-4a42-9d36-2655f8ff1f7c"
                }]
            }
        }
    '''

    def VerifySignature(self, msg: MSG):
        self.Require()
        publicKey = self.Require('PublicKey')
        msg.VerifySignature(publicKey)


    def ID(self):
        return self.Require('WalletID')


    def Notifier(self):
        return self.Require('Notifier')
    

    def QR(self):
        return self.Require('WalletQR')


    def Language(self):
        return self.Require('Language')
    

    def Locator(self):
        return self.Require('Locator')


    def HostsList(self): 
        return self.Structs('Hosts')
    

    def Hosts(self) -> STRUCT: 
        return self.Struct('Hosts', default=[])

    
    def VaultsList(self): 
        return self.Structs('Vaults')
    

    def Vaults(self) -> STRUCT: 
        return self.Struct('Vaults')
    

    def IssuersList(self): 
        return self.Structs('Issuers')
    

    def Translate(self, domains:List[STRUCT]):
        '''
        domains = [{
            "Domain": "example.com",
            "Translation": "Example Airlines"
        }]
        '''
        for lang in domains:
            for host in self.HostsList():
                if host.Att('Host') == lang.Att('Domain'):
                    host.Att('Translation', lang.Require('Translation'))
            for vault in self.VaultsList():
                if vault.Att('Vault') == lang.Att('Domain'):
                    vault.Att('Translation', lang.Require('Translation'))
            for issuer in self.IssuersList():
                if issuer.Att('Issuer') == lang.Att('Domain'):
                    issuer.Att('Translation', lang.Require('Translation'))


    def RemoveSession(self, host:str, sessionID:str):
        ''' Removes the session from the wallet '''
        root = self.Hosts().Where('Host', equals= host)
        sessions = root.Struct('Sessions')
        sessions.RemoveWhere('SessionID', equals= sessionID)

        # Remove the host, if there are no more session.
        if sessions.Lenght() == 0:
            self.Hosts().RemoveWhere(att='Host', equals=host)

        # Update the database.
        self.Update()


    def AddSession(self, host:str, sessionID:str, language:str, translation:str):
        ''' Adds the session to the wallet '''

        root = self.Hosts().Where('Host', equals= host)

        root.Merge({
            "Host": host,
            "Translation": translation,
            "Language": language,
        })

        root.AppendToAtt('Sessions', {
            "SessionID": sessionID,
            "SessionTime": self.Timestamp()
        })

        # Update the database.
        self.Update()


    def IsBoundToVault(self, vault:str) -> bool: 
        ret = self.Vaults().Where('Vault', equals= vault)
        return not ret.IsMissingOrEmpty()