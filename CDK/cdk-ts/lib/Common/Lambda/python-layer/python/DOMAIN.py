def test():
    return 'this is a DOMAIN test.'

from MANIFEST import MANIFEST

class DOMAIN:
        
    def __init__(self, domainName):
        self._domainName = domainName
        self._manifest = None
        self._manifest_yaml = None
        self._googleDns = None
    

    def Endpoint(self, path='') -> str:
        return f'https://dtfw.{self._domainName}/{path}'


    def GetManifest(self) -> any:
        '''Fetches the manifest on the domains endpoint, and returns as an object.'''

        if self._manifest:
            return self._manifest
        
        if self._manifest_yaml == None:
            endpoint = self.Endpoint('manifest')
            from WEB import WEB
            self._manifest_yaml = WEB.Get(endpoint)

        from UTILS import UTILS
        self._manifest = UTILS.FromYaml(self._manifest_yaml)

        return self._manifest
    

    def GetGoogleDns(self) -> any:
        '''
        👉️ https://developers.google.com/speed/public-dns/docs/doh
        👉️ https://developers.google.com/speed/public-dns/docs/doh/json
        👉️ https://dns.google/resolve?name=dtfw._domainkey.38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org&type=TXT&do=1
        '''

        if self._googleDns:
            return self._googleDns
        
        hostname = f'dtfw._domainkey.{self._domainName}'
        url = f'https://dns.google/resolve?name={hostname}&type=TXT&do=1'

        from WEB import WEB
        self._googleDns = WEB.GetJson(url)
        
        return self._googleDns


    def IsDnsSec(self) -> bool:
        resp = self.GetGoogleDns()
        isDnsSec = (resp['AD'] == True)
        return isDnsSec
    

    def Dkim(self) -> any:
        resp = self.GetGoogleDns()
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

