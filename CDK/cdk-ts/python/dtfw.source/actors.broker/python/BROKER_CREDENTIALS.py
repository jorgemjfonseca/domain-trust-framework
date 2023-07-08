
# 📚 BROKER_CREDENTIALS


from DTFW import DTFW
dtfw = DTFW()


class BROKER_CREDENTIALS:
    ''' 👉 https://quip.com/sN8DACFLN9wM#AfTABAujlEx '''

    # ✅ DONE
    def Issuers(self):
        ''' 👉 https://quip.com/sN8DACFLN9wM#temp:C:AfTd1f9336151234ccebad4d72ee '''
        return dtfw.DYNAMO('ISSUERS', keys=['WalletID', 'Issuer'])
    

    # ✅ DONE
    def Credentials(): 
        ''' 👉 https://quip.com/sN8DACFLN9wM#temp:C:AfTbbe653b5e8ad4f38b44dc8e7d'''
        return dtfw.DYNAMO('CREDENTIALS', keys=['WalletID', 'Issuer', 'CredentialID'])
    

    def HandleIssue(self, event):
        ''' 🐌 https://quip.com/sN8DACFLN9wM#temp:C:AfT7b35acc03fa342b9bc6e581e0 '''
        '''
        "Body": {
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",
            "CredentialID": "7bcf138b-db79-4a42-9d36-2655f8ff1f7c",
            "Code": "iata.org/SSR/WCHR",
            "Source": "https://example.com/tf/credentials/7bcf138b-db79-4a42-9d36-2655f8ff1f7c"
        }
        '''
        dtfw.MSG(event)

    
    def HandleRevoke(self, event):
        ''' 🐌 https://quip.com/sN8DACFLN9wM#temp:C:AfT9e264d13fa7b4030920efe49d '''
        '''
        "Body": {
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",
            "CredentialID": "7bcf138b-db79-4a42-9d36-2655f8ff1f7c",
            "Source": "https://example.com/tf/credentials/7bcf138b-db79-4a42-9d36-2655f8ff1f7c"
        }
        '''
        dtfw.MSG(event)


    def HandleAccepted(self, event):
        ''' 🐌 https://quip.com/sN8DACFLN9wM#temp:C:AfTe327e788ccd54eefbe5f7e844 '''
        '''
        "Body": {
            "WalletID": "1313c5c6-4038-44ea-815b-73d244eda85e",
            "CredentialID": "7bcf138b-db79-4a42-9d36-2655f8ff1f7c",
            "Issuer": "nhs.uk",
            "Code": "iata.org/SSR/WCHR",
            "Translation": "Wheelchair for ramp",
            "Path": "/storage/tf/creds/nhs.uk/7bcf138b-db79-4a42-9d36-2655f8ff1f7c"
        }
        '''
        dtfw.MSG(event)


    # ✅ DONE
    def HandleCredentials(self, event):
        ''' 🚀 https://quip.com/sN8DACFLN9wM#temp:C:AfTa9a1f10023324c448a569fa05 '''
        '''
        "Body": {
            "WalletID": "1313c5c6-4038-44ea-815b-73d244eda85e"
        }
        '''
        msg = dtfw.MSG(event)

        wallet = dtfw.BROKER().Setup().Wallets().Get(msg)
        wallet.Require()     

        '''
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
        '''
        return { 
            'Issuers': wallet.Att('Issuers', default=[])
        }


    def HandleRemove(self, event):
        ''' 🐌 https://quip.com/sN8DACFLN9wM#temp:C:AfT7c08473cd7254f24bedf5e873 '''
        '''
        "Body": {
            "WalletID": "1313c5c6-4038-44ea-815b-73d244eda85e",
            "CredentialID": "7bcf138b-db79-4a42-9d36-2655f8ff1f7c",
            "Issuer": "nhs.uk"
        }
        '''
        dtfw.MSG(event)