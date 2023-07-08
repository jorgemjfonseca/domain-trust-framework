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
    

    def GetImageQR(self, data: str) -> str:
        # 👉 https://goqr.me/api/doc/create-qr-code/
        # Example: http://api.qrserver.com/v1/create-qr-code/?size=200x200&data=🤝dtfw.org/WALLET,1,broker.com,ASD123
        base64 = self.GetImage(f'http://api.qrserver.com/v1/create-qr-code/?size=200x200&data={data}')

        # 👉 https://stackoverflow.com/questions/8499633/how-to-display-base64-images-in-html
        '''Display as 
        <img src="data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAAAUA
                AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO
                9TXL0Y4OHwAAAABJRU5ErkJggg==" alt="Red dot" />
        '''
        return base64
    

    def HttpResponse(self, code=200, body='', format='json'):
        print(f'HttpResponse: {body=}')
        print(f'HttpResponse: {format=}')

        ret = {
            'statusCode': code,
        }

        if format == 'json':
            ret['body'] = self.ToJson(body)

        elif format == 'yaml':
            ret['body'] = self.ToYaml(body)
            # contentType: text/yaml -> shows on browser (because all text/* are text)
            # contentType: application/x-yaml -> downloads (or is it application/yaml?)
            ret["headers"] = {
                "content-type": 'application/x-yaml'
            }

        elif format == 'text':
            ret['body'] = body

        else:
            ret['body'] = body

        print(f'HttpResponse: {ret=}')
        return ret