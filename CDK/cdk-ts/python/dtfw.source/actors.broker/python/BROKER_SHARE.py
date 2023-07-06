
# 📚 BROKER_SHARE

def test():
    return 'this is BROKER_SHARE test.'

from DTFW import DTFW

dtfw = DTFW()

. . .

class BROKER_SHARE:
    ''' 👉 https://quip.com/rKzMApUS5QIi#WTIABAsxxkW '''

    
    def HandleQuery(self, event):
        ''' 👉 https://quip.com/rKzMApUS5QIi#temp:C:WTI8724d650e2ae45dabb56baea4 '''
        '''
        "Body": {
            "SessionID": "125a5c75-cb72-43d2-9695-37026dfcaa48",
            "Codes": [{
                "Code": "iata.org/SSR/WCHR",
                "Vaults": [{
                    "Vault": "ec.europa.eu"
                }]
            }]
        }
        '''
        dtfw.Msg(event)

    