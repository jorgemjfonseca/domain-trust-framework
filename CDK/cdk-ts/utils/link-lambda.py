''' 📚 LINK LAMBDA ------------
Links shared lambdas to each custom lambda's folder.
This avoids adding the code to a shared custom layer.
Goal: allow code can be edited directly on the AWS console.
------------------------------- 
cd ./domain-trust-framework/CDK/cdk-ts/utils
python3 ./link-lambda.py 
------------------------------- '''


import os

path = './..'

def target_files(): 
    return [
        os.path.join(root, name)
        for root, dirs, files in os.walk(path)
        for name in files
        if '/cdk.out/' not in os.path.join(root, name) 
        if '/LAMBDA/' not in os.path.join(root, name) 
        if './lib/' in os.path.join(root, name) 
        if name.endswith(".py")
    ]

def target_dirs(): 
    return [
        os.path.join(root, name)
        for root, dirs, files in os.walk(path)
        for name in dirs
        if '/cdk.out/' not in os.path.join(root, name) 
        if '/LAMBDA/' not in os.path.join(root, name) 
        if './lib/' in os.path.join(root, name) 
        if '/lambda/' in os.path.join(root, name) 
    ]

def source_files(): 
    return [
        os.path.join(root, name)
        for root, dirs, files in os.walk(path)
        for name in files
        if './lib/Common/LAMBDA/python-layer/python/' in os.path.join(root, name) 
        if name.endswith(".py")
    ]


def IgnoreContent(files):
    # create ignore file.
    ignores = []
    files.sort()
    for f in files:
        name = f.split('/')[-1]
        ignores.append(name)
    ignores.sort()
    ignore = '\n'.join(ignores)
    return ignore


def ReplaceFile(file, content):
    fout = open(file, "wt")
    fout.write(content)
    fout.close()


def MergeIgnores(ignore, dirs):
    print ('Merging ignores...')
    dirs.sort()
    for f in dirs:
        ignore_path = f + '/.gitignore'
        Exec('rm ' + ignore_path)
        #ReplaceFile(ignore_path, ignore)
        #print(ignore_path)


def Exec(cmd):
    import subprocess
    print ('Executing ' + cmd)
    subprocess.Popen(cmd, shell=True)


def LinkFiles(dirs, files, unlink=False):
    import subprocess
    print ('Linking files...')
    dirs.sort()
    files.sort()
    for dir in dirs:
        for src in files:
            name = src.split('/')[-1]
            dst = os.path.join(dir, name)
            #print(dst)

            cmd = ''
            if unlink:
                if os.path.exists(dst):
                    cmd = f'rm {dst}'
                    print(cmd)
                    subprocess.Popen(cmd, shell=True)
            else:
                if not os.path.exists(dst):
                    base = '../../../../Common/LAMBDA/python-layer/python'
                    cmd = f'ln -s {base}/{name} {dst}'
                    print(cmd)
                    subprocess.Popen(cmd, shell=True)
            
            #return
        
def Run():
    files = source_files()
    dirs = target_dirs()
    
    ignore = IgnoreContent(files)
    MergeIgnores(ignore, dirs)
    LinkFiles(dirs, files, unlink=False)


if not os.getcwd().endswith('/CDK/cdk-ts/utils'):
    print('Run this at ./domain-trust-framewor/CDK/cdk-ts/utils')
else:
    Run()