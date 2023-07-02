import json
from urllib import request, parse
from urllib.request import urlopen



def test():
    return 'this is a WEB test.'


class WEB: 

    @staticmethod
    def Post(url: str, body: any) -> any:
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


    @staticmethod
    def Get(url: str) -> str:
        ''' 👉️ https://stackoverflow.com/questions/37819525/lambda-function-to-make-simple-http-request/71127429#71127429 '''
        print (f'WEB.Get: {url=}')

        with urlopen(url) as response:
            body = response.read()
        return body
    
    
    @staticmethod
    def GetJson(url: str) -> any:
        body = WEB.Get(url)
        return json.loads(body)