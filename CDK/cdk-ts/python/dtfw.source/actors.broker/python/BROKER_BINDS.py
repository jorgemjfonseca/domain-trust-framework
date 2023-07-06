# 📚 BROKER_BINDS

from DTFW import DTFW
dtfw = DTFW()


class BROKER_BINDS:
    ''' 👉 https://quip.com/oSzpA7HRICjq/-Broker-Binds '''

    
    # ✅ DONE
    def Binds(self):
        ''' 👉 https://quip.com/oSzpA7HRICjq#temp:C:DSDcace3164ba9e44608c1a16cb1 '''
        return dtfw.Dynamo('BINDS', keys=['WalletID', 'Vault', 'Code'])
    

    # ✅ DONE
    def Vaults(self):
        ''' 👉 https://quip.com/oSzpA7HRICjq#temp:C:DSD1ead4d286ae34b40a565e308c '''
        return dtfw.Dynamo('VAULTS', keys=['WalletID', 'Vault'])
    
    
    def HandleBindable(self, event):
        ''' 🐌 https://quip.com/oSzpA7HRICjq#temp:C:DSD2aa2718d92bf4941ac7bb41e9 '''
        '''
        "Body": {
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",
            "Binds": [{
                "Code": "iata.org/SSR/WCHR"
            }]
        }
        '''
        msg = dtfw.Msg(event)
        
        dtfw.Graph().Invoke()

    
    # ✅ DONE
    def HandleBinds(self, event):
        ''' 🚀 https://quip.com/oSzpA7HRICjq#temp:C:DSD0d59568b34f74ef0a2df28896 '''
        '''
        "Body": {
          "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a"
        }
        '''
        msg = dtfw.Msg(event)

        wallet = dtfw.Broker().Setup().Wallets().Get(msg)
        wallet.Require()      

        '''
        {
            "Vaults": [{
                "Vault": "iata.org",
                "Translation": "IATA",
                "Binds": [{
                    "BindID": "793af21d-12b1-4cea-8b55-623a19a28fc5",
                    "Code": "iata.org/SSR/WCHR",
                    "Translation": "Wheelchair for ramp"
                }]
            }],
        }
        '''
        return { 
            'Hosts': wallet.Att('Vaults', default=[])
        }   


    def HandleBound(self, event):
        ''' 🐌 https://quip.com/oSzpA7HRICjq/-Broker-Binds#temp:C:DSD3f7309f961e24f0ebb5897e2f '''
        '''
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "Request": {...},
            "Binds": [{
                "BindID": "793af21d-12b1-4cea-8b55-623a19a28fc5",
                "Code": "iata.org/SSR/WCHR"
            }]
        }
        '''
        dtfw.Msg(event)


    def HandleUnbind(self, event):
        ''' 🐌 https://quip.com/oSzpA7HRICjq#temp:C:DSDcd716c71b51c4c528a8c218fd '''
        '''
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "BindID": "793af21d-12b1-4cea-8b55-623a19a28fc5"
        }
        '''
        dtfw.Msg(event)
