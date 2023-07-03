# 📚 DOMAIN

from DTFW import DTFW
dtfw = DTFW()


def test():
    return 'this is a DOMAIN test.'


class DOMAIN:
        
    def __init__(self, domain:str=None):
        self._domain = domain
        self._manifest = None
        self._yaml = None
        self._google = None
    

    def Endpoint(self, path='') -> str:
        return f'https://dtfw.{self._domain}/{path}'


    def Manifest(self) -> any:
        '''Fetches the manifest on the domains endpoint, and returns as an object.'''

        if self._manifest:
            return self._manifest
        
        if self._yaml == None:
            endpoint = self.Endpoint('manifest')
            
            self._yaml = dtfw.Web().Get(endpoint)

        self._manifest = dtfw.Utils().FromYaml(self._yaml)

        return self._manifest
    

    def GoogleDns(self) -> any:
        '''
        👉️ https://developers.google.com/speed/public-dns/docs/doh
        👉️ https://developers.google.com/speed/public-dns/docs/doh/json
        👉️ https://dns.google/resolve?name=dtfw._domainkey.38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org&type=TXT&do=1
        '''

        if self._google:
            return self._google
        
        hostname = f'dtfw._domainkey.{self._domain}'
        url = f'https://dns.google/resolve?name={hostname}&type=TXT&do=1'

        self._google = dtfw.Web().GetJson(url)
        
        return self._google


    def IsDnsSec(self) -> bool:
        resp = self.GoogleDns()
        isDnsSec = (resp['AD'] == True)
        return isDnsSec
    

    def Dkim(self) -> any:
        resp = self.GoogleDns()
        dkim = None
        exists = 'Answer' in resp
        if exists:
            for answer in resp['Answer']:
                if answer['type'] == 16:
                    dkim = answer['data']
        return dkim


    def IsDkimSetUp(self) -> bool:
        return self.Dkim() != None
    

    def PublicKey(self) -> str:
        dkim = self.Dkim()
        public_key = None
        for part in dkim.split(';'):
            elems = part.split('=')
            if elems[0] == 'p' and len(elems) == 2:
                public_key = elems[1];
        return public_key
    

    def HasPublicKey(self) -> bool:
        public_key = self.PublicKey()
        return public_key != None
