
# 📚 BROKER_SESSIONS


from DTFW import DTFW
from MSG import MSG
dtfw = DTFW()
        


class BROKER_SESSIONS:
    ''' 👉 https://quip.com/HrgkAuQCqBez#bXDABAe5brB '''


    # ✅ DONE
    def Hosts(): 
        return dtfw.Dynamo('HOSTS', keys=['WalletID', 'Host'])
    
    
    # ✅ DONE
    def Sessions(): 
        return dtfw.Dynamo('SESSIONS', keys=['WalletID', 'Host', 'SessionID'])
    

    # ✅ DONE
    def Translate(self, msg:MSG):
        '''
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "Language": "en-us"
        }
        '''
        wallet = dtfw.Broker().Setup().Wallets().Get(msg)

        hosts = wallet.Structs('Hosts')
        '''
            "Hosts": [{
                "Host": "iata.org",
                "Translation": "IATA",
                "Language": "en-us",
                "Sessions": []
            }]
        '''

        domains = []
        for host in hosts:
            domains.append(host.Require('Host'))

        ret = dtfw.Graph().InvokeTranslate({
            "Language": msg.Require('Language'),
            "Domains": domains
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

        for host in wallet.Structs('Hosts'):
            for lang in ret.Structs('Domains'):
                if host.Att('Host') == lang.Att('Domain'):
                    host.Att('Translation', lang.Require('Translation'))

        wallet.Update()


    # ✅ DONE
    def HandleSessions(self, event):
        ''' 👉 https://quip.com/HrgkAuQCqBez#temp:C:bXD09ae7595fe4943d5985d83fd0 '''
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
            "Hosts": [{
                "Host": "iata.org",    
                "Translation": "IATA",
                "Sessions": [{
                    "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",
                    "SessionTime": "2018-12-10T13:45:00.000Z"
                }]
            }]
        }
        '''
        return { 
            'Hosts': wallet.Att('Hosts', default=[])
        }


    def HandleTalker(self, event):
        ''' 👉 https://quip.com/HrgkAuQCqBez#temp:C:bXDff3472e2ec4d4733bd1b38141 '''
        '''
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "Host": "iata.org",
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48"
        }
        '''
        dtfw.Msg(event)
    

    def HandleCheckout(self, event):
        ''' 👉 https://quip.com/HrgkAuQCqBez#temp:C:bXDca9dada42bf6431daed5f1c07 '''
        '''
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "Host": "iata.org",
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48"
        }
        '''
        dtfw.Msg(event)
    

    def HandleAbandon(self, event):
        ''' 👉 https://quip.com/HrgkAuQCqBez#temp:C:bXD2d6cd3790047405c89019c170 '''
        '''
        "Body": {
            "WalletID": "61738d50-d507-42ff-ae87-48d8b9bb0e5a",
            "Host": "iata.org",
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48"
        }
        '''
        dtfw.Msg(event)
    

    def HandleAssess(self, event):
        ''' 👉 https://quip.com/HrgkAuQCqBez#temp:C:bXD4396f26fefe34874a12828c36 '''
        '''
        "Body": {
            "QR": "🤝dtfw.org/QR,1,any-printer.com,7V8KD3G"
        }
        '''
        dtfw.Msg(event)
    

    def HandleGoodbye(self, event):
        ''' 👉 https://quip.com/HrgkAuQCqBez#temp:C:bXD9f09e5f058ee4fc8a77be4ebe '''
        '''
        "Body": {
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",
            "Message": "Parking ended for vehicle AB-12-34.".
        }
        '''
        dtfw.Msg(event)
    

    