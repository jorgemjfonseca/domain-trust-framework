# 📚 MANIFEST

from DTFW import DTFW
dtfw = DTFW()


def test():
    return 'this is a MANIFESTER test.'


class MANIFESTER:
        

    def HandleAlerter(self, event):
        # 👉️ https://docs.aws.amazon.com/appconfig/latest/userguide/working-with-appconfig-extensions-about-predefined-notification-sqs.html

        '''
        {
        "Type":"OnDeploymentComplete"
        }
        '''
        print(f'{event=}')
    
        if event['Type'] == 'OnDeploymentComplete':
            print('send message to Listener')


    def _viewer(self, format):
        manifest = dtfw.Manifest().FromAppConfig()
        return dtfw.Utils().HttpResponse(body=manifest, format=format)


    def HandleYamlViewer(self):
        return self._viewer('yaml')
    

    def HandleJsonViewer(self):
        return self._viewer('json')
    

    def HandleDefaultViewer(self):
        return self._viewer('text')