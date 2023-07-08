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


    def HandleRegisterer(self):
        ''' 👉 host -t NS 105b4478-eaa5-4b73-b2a5-4da2c3c2dac0.dev.dtfw.org '''
        print(f'register_domain')

        import os
        hosted_zone_id = os.environ['hostedZoneId']  

        zone = dtfw.ROUTE53(hosted_zone_id)

        domain = zone.Domain()
        serverList = zone.NameServerList()
        dnsSec = zone.AddDX()
        dtfwOrg = 'z6jsx3ldteaiewnhm4dwuhljzi0vrxgn.lambda-url.us-east-1.on.aws'

        url = f'https://{dtfwOrg}/?domain={domain}&servers={serverList}&dnssec={dnsSec}'
        dtfw.Web().Get(url)


    def HandleNamerCreate(self):
        ''' 
        Generate a new Random name, if one doesn't yet exist.
        If it already exists, then ignore.
        👉 https://www.sufle.io/blog/how-to-use-ssm-parameter-store-with-boto3
        '''

        import os
        paramName = os.environ['paramName']
        domainName = os.environ['domainName']
        
        try:
            param = dtfw.SSM().Get(paramName)
        except:
            param = None

        if (param):
            print(f'Parameter already set, ignoring: ' + param)
            return
        else:
            print(f'Setting new parameter: ' + domainName)
            dtfw.SSM().Set(paramName, domainName)


    def HandleNamerDelete(self):
        import os
        paramName = os.environ['paramName']
        dtfw.SSM().Delete(paramName)
