# 📚 DKIM (part of SYNCAPI)

from DTFW import DTFW
dtfw = DTFW()


def test():
    return 'this is SYNCAPI.DKIM test.'


class VALIDATOR():

    def __init__(self, obj):
        self._obj = obj

    def Hash(self) -> str:
        return self._obj['hash']
        
    def IsVerified(self) -> bool:
        return self._obj['isVerified']
        

class DKIM:
    

    # REQUEST { text, publicKey, signature }
    # RESPONSE { hash, isVerified }
    def ValidateSignature(self, text, publicKey, signature) -> VALIDATOR:
        print(f'{self._elapsed()} Invoking validator...')

        ret = dtfw.LAMBDA('VALIDATOR_FN').Invoke({
            'text': text,
            'publicKey': publicKey,
            'signature': signature
        })
        
        return VALIDATOR(ret)
    

    def HandleDkimCfn(self): 
        dtfw.LAMBDA('KeyPairRotatorFn').Invoke()


    def HandleDkimSetter(self, event):
        # 👉 https://repost.aws/knowledge-center/route53-resolve-dkim-text-record-error

        print(f'{event=}')
        import os

        key = event['public_key']
        key = key.replace('-----BEGIN PUBLIC KEY-----', '')
        key = key.replace('-----END PUBLIC KEY-----', '')
        key = key.replace('\n', '')

        dkim = key[:200] + '""' + key[200:]
        hostedZoneId= os.environ['hostedZoneId']

        dtfw.ROUTE53(hostedZoneId).AddTXT(
            record_name = os.environ['dkimRecordName'], 
            value = f'"v=DKIM1;k=rsa;p={dkim};"')    
        
        
    def HandleKeyPairRotator(self):
        # Get the keys
        keys = dtfw.LAMBDA('KeyPairGeneratorFn').Invoke()
        print(f'{keys=}')

        # Set Route53 DKIM with public key
        dtfw.LAMBDA('DkimSetterFn').Invoke({
            'public_key': keys['publicKey']
        })

        # Store the key pair in Secrets Manager
        dtfw.LAMBDA('SecretSetterFn').Invoke(keys)


    def HandleSecretSetter(self, event):
        '''
        {
            "publicKey": "my-public-key",
            "privateKey": "my-private-key"
        }
        '''
        print(f'{event=}')

        dtfw.SECRETS().Set('/dtfw/publicKey', value=event['publicKey'])
        dtfw.SECRETS().Set('/dtfw/privateKey', value=event['privateKey'])


    def HandleSetAlias(self):
        import os
        r53 = dtfw.ROUTE53(os.environ['hostedZoneId'])

        r53.AddApiGW(
            customDomain = os.environ['customDomain'], 
            apiHostedZoneId = os.environ['apiHostedZoneId'],
            apiAlias = os.environ['apiAlias'])
    