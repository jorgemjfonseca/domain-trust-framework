# 📚 BIND

def test():
    return 'this is a BIND test.'


from STRUCT import STRUCT
from DTFW import DTFW

dtfw = DTFW()


class BIND(STRUCT):
    ''' 👉 https://quip.com/IZapAfPZPnOD#temp:C:PDZ43b66f9fe581460e907436cd8 '''

    def Code(self):
        return self.Require('Code')


