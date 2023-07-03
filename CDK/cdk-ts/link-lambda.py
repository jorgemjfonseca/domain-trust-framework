import os

path = '.'

target_files = [
    os.path.join(root, name)
    for root, dirs, files in os.walk(path)
    for name in files
    if '/cdk.out/' not in os.path.join(root, name) 
    if '/LAMBDA/' not in os.path.join(root, name) 
    if './lib/' in os.path.join(root, name) 
    if name.endswith(".py")
]

target_dirs = [
    os.path.join(root, name)
    for root, dirs, files in os.walk(path)
    for name in dirs
    if '/cdk.out/' not in os.path.join(root, name) 
    if '/LAMBDA/' not in os.path.join(root, name) 
    if './lib/' in os.path.join(root, name) 
    if '/lambda/' in os.path.join(root, name) 
]

source_files = [
    os.path.join(root, name)
    for root, dirs, files in os.walk(path)
    for name in files
    if './lib/Common/LAMBDA/python-layer/python/' in os.path.join(root, name) 
    if name.endswith(".py")]


def IgnoreContent(files):
    # create ignore file.
    ignores = []
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
    for f in dirs:
        ignore_path = f + '/.gitignore'
        ReplaceFile(ignore_path, ignore)
        #print(ignore_path)

def LinkFiles(dirs, files):
    import subprocess
    print ('Linking files...')
    for dir in dirs:
        for src in files:
            name = src.split('/')[-1]
            dst = os.path.join(dir, name)
            #print(dst)

            #os.symlink(src, dst)
            base = '../../../../Common/LAMBDA/python-layer/python'
            cmd = f'ln -s {base}/{name} {dst}'
            print(cmd)
            subprocess.Popen(cmd, shell=True)
            return
        

ignore = IgnoreContent(files=source_files)
MergeIgnores(ignore, dirs=target_dirs)
LinkFiles(dirs=target_dirs, files=source_files)