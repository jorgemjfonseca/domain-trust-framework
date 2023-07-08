
# 📚 BROKER_SHARE

from DTFW import DTFW


class BROKER_SHARE(DTFW):
    ''' 🤵📎 https://quip.com/rKzMApUS5QIi#WTIABAsxxkW '''

    
    def HandleQuery(self, event):
        ''' 🐌 https://quip.com/rKzMApUS5QIi#temp:C:WTI8724d650e2ae45dabb56baea4 '''
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
        self.MSG(event)

        # SUBSET = Call 🚀 Queryable: 🕸 Graph
        #    * Host: ♌ From: ✉️ Msg
        #    * Binds[]: 🪣 Binds: 🤵📎 Broker. Binds 
        #    * Credentials[]: 🪣 Credentials: 🤵📎 Broker. Credentials
        # Filter:
        #    * For all credentials, only show the ones that are active - i.e., within the start and expiration date.
        #    * For the following credentials types, only show the credentials issued by the consumer itself:
        #        * 🧩 //BOOKING/SELF: 🤝🤗 Host.DTFW.org
        #        * 🧩 //ORDER/SELF: 🤝🤗 Host.DTFW.org
        # With the resulting subset
        #    * Add to 🪣 Queries
        #    * Call 🚀 Translate: 🕸 Graph
        #    * Forward to 🐌 Query: 📣 Notifier
    