# 📚 SYNCAPI

from DTFW import DTFW
dtfw = DTFW()


def test():
    return 'this is SYNCAPI test.'


class SYNCAPI:
    
    
    def Send(self, event: any): 

        msg = dtfw.Msg(event)
        msg.Stamp()
        envelope = msg.Envelope()

        sent = dtfw.Lambda('SENDER').Invoke(envelope)
        return sent


    def HandleDkimCfn(self): 
        dtfw.Lambda('KeyPairRotatorFn').Invoke()


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

        dtfw.Route53(hostedZoneId).AddTXT(
            record_name = os.environ['dkimRecordName'], 
            value = f'"v=DKIM1;k=rsa;p={dkim};"')    
        
        
    def HandleKeyPairRotator(self):
        # Get the keys
        keys = dtfw.Lambda('KeyPairGeneratorFn').Invoke()
        print(f'{keys=}')

        # Set Route53 DKIM with public key
        dtfw.Lambda('DkimSetterFn').Invoke({
            'public_key': keys['publicKey']
        })

        # Store the key pair in Secrets Manager
        dtfw.Lambda('SecretSetterFn').Invoke(keys)


    def HandleSecretSetter(self, event):
        '''
        {
            "publicKey": "my-public-key",
            "privateKey": "my-private-key"
        }
        '''
        print(f'{event=}')

        dtfw.Secrets().Set('/dtfw/publicKey', value=event['publicKey'])
        dtfw.Secrets().Set('/dtfw/privateKey', value=event['privateKey'])


    def HandleSetAlias(self):
        import os
        r53 = dtfw.Route53(os.environ['hostedZoneId'])

        r53.AddApiGW(
            customDomain = os.environ['customDomain'], 
            apiHostedZoneId = os.environ['apiHostedZoneId'],
            apiAlias = os.environ['apiAlias'])