''' 📚 RENAME INDEX ------------
------------------------------- 
cd ./domain-trust-framework/CDK/cdk-ts/utils
python3 ./link-lambda.py 
------------------------------- '''


import os

path = './..'

def target_dirs(): 
    return [
        os.path.join(root, name)
        for root, dirs, files in os.walk(path)
        for name in files
        if '/cdk.out/' not in os.path.join(root, name) 
        if '/LAMBDA/' not in os.path.join(root, name) 
        if './lib/' in os.path.join(root, name) 
        if '/lambda/' in os.path.join(root, name) 
        if name.endswith("index.py")
        if not name.endswith("_index.py")
    ]



def RenameFiles(files):
    import subprocess
    print ('Linking files...')
    files.sort()
    for src in files:
        dst = src.replace('/index.py', '/_index.py')
        cmd = f'mv {src} {dst}'
        print(cmd)
        subprocess.Popen(cmd, shell=True)
        #return
        

def Run():
    files = target_dirs()
    RenameFiles(files)


if not os.getcwd().endswith('/CDK/cdk-ts/utils'):
    print('Run this at ./domain-trust-framewor/CDK/cdk-ts/utls')
else:
    Run()