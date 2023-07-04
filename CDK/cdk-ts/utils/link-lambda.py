''' 📚 LINK LAMBDA ------------
Links shared lambdas to each custom lambda's folder.
This avoids adding the code to a shared custom layer.
Goal: allow code can be edited directly on the AWS console.
------------------------------- 
cd ./domain-trust-framework/CDK/cdk-ts/utils
python3 ./link-lambda.py 
------------------------------- '''


import os
import sys

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
        if './python/dtfw/python/' in os.path.join(root, name) 
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

        if os.path.exists(ignore_path):
            Exec('rm -f ' + ignore_path)

        #ReplaceFile(ignore_path, ignore)
        #print(ignore_path)

        ReplaceFile('./../lib/.gitignore', ignore)


def Exec(cmd, silent=True):
    import subprocess
    if not silent:
        print ('Executing ' + cmd)
    process = subprocess.Popen(cmd, shell=True)
    process.wait()


def LinkFiles(dirs, files, unlink=False):
    import subprocess
    print ('Linking files4...')
    dirs.sort()
    files.sort()

    if unlink:
        print('Unlinking files2...')
    else:
        print('Linking files3...')

    for dir in dirs:
        for src in files:
            name = src.split('/')[-1]
            dst = os.path.join(dir, name)
            #print(dst)

            cmd = ''
            if unlink:
                #print('Unlinking files...')
                #print(f'unlinking {dst}')
                if True or os.path.exists(dst):
                    cmd = f'rm -f {dst}'
                    #print(cmd)
                    Exec(cmd)
            else:
                #print('Linking files...')
                if not os.path.exists(dst):
                    base = '../../../../../python/dtfw/python'
                    cmd = f'ln -s {base}/{name} {dst}'
                    #print(cmd)
                    Exec(cmd)
            
    print('Done!')
    #return
        
def Run():
    files = source_files()
    dirs = target_dirs()
    
    ignore = IgnoreContent(files)
    MergeIgnores(ignore, dirs)

    unlink = False
    if len(sys.argv) > 1:
        if sys.argv[1] == 'unlink':
            unlink = True
            
    LinkFiles(dirs, files, unlink)


if not os.getcwd().endswith('/CDK/cdk-ts/utils'):
    print('Run this at ./domain-trust-framewor/CDK/cdk-ts/utils')
else:
    Run()