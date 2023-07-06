# 📚 WEB

import json
from urllib import request, parse
from urllib.request import urlopen
import base64


def test():
    return 'this is a WEB test.'


class WEB: 

    def Post(self, url: str, body: any) -> any:
        ''' 👉️ https://stackoverflow.com/questions/36484184/python-make-a-post-request-using-python-3-urllib  '''
    
        print(f'{url=}')
        print(f'body={json.dumps(body)}')

        # data = parse.urlencode(body).encode()
        # print(f'{data=}')
        data = bytes(json.dumps(body), encoding='utf-8')
        
        req = request.Request(url=url, method='POST', data=data)
        req.add_header('Content-Type', 'application/json')
        resp = request.urlopen(req)
        
        charset=resp.info().get_content_charset()
        if charset == None:
            charset = 'utf-8'
        content=resp.read().decode(charset)
        
        print(f'{content=}')
        return content


    def Get(self, url: str) -> str:
        ''' 👉️ https://stackoverflow.com/questions/37819525/lambda-function-to-make-simple-http-request/71127429#71127429 '''
        print (f'WEB.Get: {url=}')

        with urlopen(url) as response:
            body = response.read()
        return body
    
    
    def GetJson(self, url: str) -> any:
        body = WEB.Get(url)
        return json.loads(body)
    

    def GetImage(self, url: str) -> str:
        ''' 👉️ https://stackoverflow.com/questions/38408253/way-to-convert-image-straight-from-url-to-base64-without-saving-as-a-file-in-pyt '''
        print (f'WEB.GetImage: {url=}')
        
        return base64.b64encode(urlopen(url).read())