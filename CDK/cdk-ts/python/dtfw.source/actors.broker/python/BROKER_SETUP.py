
# 📚 BROKER_SETUP

from BROKER import BROKER
from BROKER_BASE import BROKER_BASE

from DTFW import DTFW
from STRUCT import STRUCT
from WALLET import WALLET


# ✅ DONE
class BROKER_SETUP(BROKER_BASE):
    ''' 👉 https://quip.com/zaYoA4kibXAP/-Broker-Setup '''


    # ✅ DONE
    def HandleOnboard(self, event):
        ''' 📣🚀 https://quip.com/zaYoA4kibXAP#temp:C:DQN1f2d80d98fdd4e69a98a32887 
        "Body": {
            "Language": "en-us",
            "PublicKey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDH+wPrKYG1KVlzQUVtBghR8n9dzcShSZo0+3KgyVdOea7Ei7vQ1U4wRn1zlI5rSqHDzFitblmqnB2anzVvdQxLQ3UqEBKBfMihnLgCSW8Xf7MCH+DSGHNvBg2xSNhcfEmnbLPLnbuz4ySn1UB0lH2eqxy50zstxhTY0binD9Y+rwIDAQAB"
        }
        '''
        msg = self.MSG(event) 
        
        walletID = self.UUID()
        brokerDomain = self.Domain()
        
        self.Wallets().Insert({
            'ID': walletID,
            'Language': msg.Require('Language'),
            'PublicKey': msg.Require('PublicKey'),
            'Notifier': msg.From()
        })

        return {
            "WalletID": walletID
        }

    
    # ✅ DONE
    def HandleTranslate(self, event):
        ''' 🧑‍🦰🐌 https://quip.com/zaYoA4kibXAP#temp:C:DQN0cc419509625497ea39fa08e9 
        "Header" {
            "From": "61738d50-d507-42ff-ae87-48d8b9bb0e5a"
        },
        "Body": {
            "Language": "en-us"
        }
        '''
        msg, wallet = self.VerifyWalletSignature(event)

        # Call 🚀 Translate: 🕸 Graph for:
        domains = []
        codes = []
        for session in self.SessionsOf(wallet):
            domains.append(session.HostDomain())
        for bind in self.BindsOf(wallet):
            domains.append(bind.VaultDomain())
            codes.append(bind.CodeCode())
        for credential in self.CredentialsOf(wallet):
            domains.append(credential.IssuerDomain())
            codes.append(credential.CodeCode())

        ret = self.GRAPH().InvokeTranslate(
            language= msg.Require('Language'),
            domains= domains,
            codes= codes
        )
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

        # Translate the wallet domains.
        for lang in ret.Structs('Domains'):
            translation = lang.RequireStr('Translation')
            domain = lang.RequireStr('Domain')
            for session in self.SessionsOf(wallet):
                if session.HostDomain() == domain:
                    session.HostTranslation(translation)
            for bind in self.BindsOf(wallet):
                if bind.VaultDomain() == domain:
                    bind.VaultTranslation(translation)
            for credential in self.CredentialsOf(wallet):
                if credential.IssuerDomain() == domain:
                    credential.IssuerTranslation(translation)

        # Translate the wallet codes.
        for lang in ret.Structs('Codes'):
            translation = lang.RequireStr('Translation')
            code = lang.RequireStr('Code')
            for bind in self.BindsOf(wallet):
                if bind.CodeCode() == code:
                    bind.CodeTranslation(translation)
            for credential in self.CredentialsOf(wallet):
                if credential.CodeCode() == code:
                    credential.CodeTranslation(translation)

        # Call 🐌 Translated: 📣 Notifier
        self.NOTIFIER().Invoke(
            notifier= wallet.Require('Notifier'),
            data= {
                "WalletID": wallet.ID(),
                "Language": msg.Require('Language')
            },
            source= 'Broker-Translate'
        )