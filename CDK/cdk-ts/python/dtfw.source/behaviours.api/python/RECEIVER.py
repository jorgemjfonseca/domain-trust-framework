# 📚 RECEIVER (part of SYNCAPI)

import os
import json

from MSG import MSG

from DTFW import DTFW
dtfw = DTFW()


class RECEIVER:

    def __init__(self):
        self._timer = dtfw.Timer()

    def _elapsed(self):
        return self._timer.Elapsed()


    # REQUEST { hostname }
    # RESPONSE: str
    def _invokeDkimReader(self, envelope, checks):
        print(f'{self._elapsed()} Invoke dns.google...')

        domain = dtfw.Msg(envelope).From()
        hostname = f'dtfw._domainkey.{domain}'
        checks.append(f'Valid domain?: {hostname}')
        
        d = dtfw.Domain(domain)
        d.GoogleDns()
        print(f'{self._elapsed()} Validate dns.google...')

        isDnsSec = d.IsDnsSec()
        checks.append(f'IsDnsSec?: {isDnsSec}')
        if not isDnsSec:
            raise Exception(f"Sender is not DNSSEC protected.")

        isDkimSetUp = d.IsDkimSetUp()
        checks.append(f'DKIM set?: {isDkimSetUp}')
        if not isDkimSetUp:
            raise Exception(f"Sender DKIM not found for dtfw.")
        
        hasPublicKey = d.HasPublicKey()
        checks.append(f'Public Key set?: {hasPublicKey}')
        if not hasPublicKey:
            raise Exception(f"Public key not found on sender DKIM.")
        
        return d.PublicKey()
        

    def _validateTo(self, msg: MSG, checks):
        to = msg.To().lower()
        me = os.environ['DOMAIN_NAME'].lower()

        if to != me:
            raise Exception(f'Wrong domain. Expected [{me}], but received [{to}]!')
        checks.append(f'For me?: {True}')
    

    def _validateHashAndSignature(self, msg: MSG, checks, speed):
        print(f'{self._elapsed()} Validating signature...')
        
        started = self._timer.StartWatch()
        publicKey = self._invokeDkimReader(msg.Envelope(), checks)
        speed['Get DKIM over DNSSEC'] = self._timer.StopWatch(started)

        started = self._timer.StartWatch()
        msg.VerifySignature(publicKey)
        checks.append(f'Hash and Signature match?: {True}')
        speed['Verify signature'] = self._timer.StopWatch(started)


    def _validate(self, msg, speed):
        print(f'{self._elapsed()} Validating...')
        
        error = None
        checks = []
        
        try:
            msg.ValidateHeader()
            self._validateTo(msg, checks)
            self._validateHashAndSignature(msg, checks, speed) 

        except Exception as e:
            if hasattr(e, 'message'):
                error = f'{e.message}'
            else:
                error = f'{e}'
        
        ret = {
            'Error': error,
            'Checks': checks
        }

        print(f'{ret=}')
        return ret


    def _execute(self, validation, envelope, speed):
        print(f'{self._elapsed()} Executing...')
        started = self._timer.StartWatch()

        if validation['Error']:
            ret = { 
                'Result': 'Ignored, invalid envelope!'
            }
            print(f'{ret=}')
            return ret

        msg = dtfw.Msg(envelope)
        subject = msg.Subject()
        target = dtfw.Dynamo().Get(subject)
        
        answer = None 
        if (target):
            answer = dtfw.Lambda(target['Target']).Invoke(envelope)

        ret = {
            'Result': 'Executed',
            'Target': target,
            'Answer': answer
        }    
        print(f'{ret=}')

        speed['Execute method'] = self._timer.StopWatch(started)
        return ret


    def output(self, envelope, validation, execution, speed):
        print(f'{self._elapsed()} Building the output...')

        output = {}
        if execution != None and 'Answer' in execution:
            output = execution['Answer']

        output['Insights'] = {
            'Speed': speed,
            'Execution': execution,
            'Validation': validation,
            'Received': envelope
        }

        print ('Returning...')
        if validation['Error']:
            return dtfw.Utils().HttpResponse(400, output)
        return dtfw.Utils().HttpResponse(200, output)


    def _parse(self, event):
        envelope = {}
        if 'httpMethod' not in event:
            envelope = event
        elif 'body' in event and event['body'] != None:
            envelope = json.loads(event['body'])
        elif event['httpMethod'] == 'GET':
            envelope = {}

        return envelope 


    def Handle(self, event, context):
        '''
        {
            "Header":{
                "Correlation":"bb37d258-015c-497e-8a67-50bf244a9299",
                "Timestamp":"2023-06-24T23:08:24.550719Z",
                "To":"105b4478-eaa5-4b73-b2a5-4da2c3c2dac0.dev.dtfw.org",
                "Subject":"AnyMethod",
                "Code":"dtfw.org/msg",
                "Version":"1",
                "From":"105b4478-eaa5-4b73-b2a5-4da2c3c2dac0.dev.dtfw.org"
            },
            "Body":{
            },
            "Signature": "Lw7sQp6zkOGyJ+OzGn+B1R4rCN/qcYJCtijflQu1Ayqpgxph10yS3KwA4yRhjXgUovskK7LSH+ZqhXm1bcLeMS81l1GKDVaZk3qXpNtrwRmnWrjfD1MekZrO1sRWPNBRH157INAkPWFH/Wb2LLPCAJZYwIv02BF3zKz/Zgm8z7BqOJ3ZrAOC80kTef1zhXNXUMQ/HBrspUTx0NFiMi+dXZMJ69ylxGaAjALMLmcMwFqH2D5cWqX5+eMx0zv2tMh73e8xQqxOr+YLUkO7JjK56KbCUk0HYGUbL5co9eyQMYCGyDtn0G2FqSK9h8BJ1YW3LQmWWTGa/kWDxPjHR3iNyg==", 
            "Hash": "ee6ca2a43ec05d0bd855803407b9350e6c84dd1b981274e51ce0a0a8be16e4a1"
        }
        '''
        print(f'{event=}')

        envelope = self._parse(event)
        print(f'{envelope=}')
        if envelope == {}:
            return dtfw.Utils().HttpResponse(200, { 'Result': 'Inbox is working :)' })

        speed = {}
        started = self._timer.StartWatch()
        msg = dtfw.Msg(envelope)
        validation = self._validate(msg, speed)
        execution = self._execute(validation, envelope, speed)
        speed['Total handling'] = self._timer.StopWatch(started)

        return self.output(envelope, validation, execution, speed)
