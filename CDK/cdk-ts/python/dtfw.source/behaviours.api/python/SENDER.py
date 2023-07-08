# 📚 SENDER (part of SYNCAPI)
# 👉️ https://quip.com/NiUhAQKbj7zi


from DTFW import DTFW
dtfw = DTFW()


class SENDER:

    
    def _sign(self, privateKey: str, publicKey, text) -> str:
        ''' 👉️ https://hands-on.cloud/boto3-kms-tutorial/ '''
        # REQUEST { privateKey, publicKey, text }
        # RESPONSE { hash, signature, isVerified }
        return dtfw.LAMBDA('SIGNER_FN').Invoke({
            'privateKey': privateKey,
            'publicKey': publicKey,
            'text': text
        })
        

    def _get_keys(self): 
        return {
            'publicKey': dtfw.SECRETS().Get('/dtfw/publicKey'),
            'privateKey': dtfw.SECRETS().Get('/dtfw/privateKey')
        }


    def _wrap_envelope(self, message: any):
        import os
        
        defaults = {
            'Header': {
                'Correlation': dtfw.UTILS().Correlation(),
                'Timestamp': dtfw.UTILS().Timestamp()
            },
            'Body': {}
        }
        print(f'{defaults=}')
        
        overrides = {
            'Header': {
                'Code': 'dtfw.org/msg', 
                'Version': '1',
                'From': os.environ['DOMAIN_NAME']
            }
        }
        print(f'{overrides=}')

        # 👉️ https://stackoverflow.com/questions/14839528/merge-two-objects-in-python
        envelope = defaults
        envelope['Header'].update(message['Header']) 
        envelope['Header'].update(overrides['Header'])
        if 'Body' in message:
            envelope['Body'].update(message['Body']) 

        return envelope


    def _sign_envelope(self, envelope: any):
        
        keys = self._get_keys()
        
        canonicalized = dtfw.UTILS().Canonicalize(envelope)

        signed = self._sign(
            privateKey=keys['privateKey'], 
            publicKey=keys['publicKey'], 
            text=canonicalized)

        if not signed['isVerified']:
            raise Exception('The sending signature is not valid!')
        
        envelope.update({
            'Signature': signed['signature'],
            'Hash': signed['hash']
        })

        return envelope


    def _send_envelope(self, envelope: any):

        to = dtfw.MSG(envelope).To()
        url = f'https://dtfw.{to}/inbox'
        
        return dtfw.Web.Post(url, envelope)

    
    def Handle(self, event):
        ''' 👉️ https://quip.com/NiUhAQKbj7zi '''

        '''
        { 
            "Header": {
                "To": "7b61af20-7518-4d5a-b7c0-eee17e54bf7a.dev.dtfw.org",
                "Subject": "AnyMethod"
            }
        }
        '''    
        print(f'{event=}')

        message = event
        envelope = self._wrap_envelope(message)
        envelope = self._sign_envelope(envelope)
        sent = self._send_envelope(envelope)
        return sent