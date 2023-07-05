# 📚 WALLET

def test():
    return 'this is WALLET test.'


from ITEM import ITEM
from MSG import MSG
from DTFW import DTFW

dtfw = DTFW()


class WALLET(ITEM):


    def ValidateSignature(self, msg: MSG):
        publicKey = self.Require('PublicKey')
        msg.ValidateSignature(publicKey)


