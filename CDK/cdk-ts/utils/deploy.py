''' 📚 DEPLOY
'''

import os
import sys


def Exec(cmd):
    import subprocess
    print ('Executing ' + cmd)
    process = subprocess.Popen(cmd, shell=True)
    process.wait()

        
def Run():
    if len(sys.argv) < 2:
        print('pass the stack name as argument')
        return
    
    stack = sys.argv[1] 
    if stack == 'env':
        Exec('isengardcli assume dtfw+authority@amazon.com --region eu-west-1')
    else:
        Exec('python3 link-lambda.py')
        Exec(f'cdk deploy {stack} --require-approval never')
        Exec('python3 link-lambda.py unlink')



if not os.getcwd().endswith('/CDK/cdk-ts/utils'):
    print('Run this at ./domain-trust-framewor/CDK/cdk-ts/utils')
else:
    Run()