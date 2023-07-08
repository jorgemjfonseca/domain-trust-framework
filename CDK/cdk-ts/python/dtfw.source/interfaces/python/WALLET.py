# 📚 WALLET

def test():
    return 'this is WALLET test.'


from STRUCT import STRUCT
from MSG import MSG
from DTFW import DTFW

dtfw = DTFW()


class WALLET(STRUCT):


    def ValidateSignature(self, msg: MSG):
        publicKey = self.Require('PublicKey')
        msg.VerifySignature(publicKey)


