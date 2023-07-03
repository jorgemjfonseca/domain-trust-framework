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

for f in source_files:
    #print(f)
    pass

# create ignore file.
ignores = []
for f in source_files:
    ignores.append(f.split('/')[-1])
ignores.sort()
ignore = '\n'.join(ignores)


def ReplaceFile(file, content):
    fout = open(file, "wt")
    fout.write(content)
    fout.close()


print ('Merging ignores...')
for f in target_dirs:
    ignore_path = f + '/.gitignore'
    #print(ignore_path)

ReplaceFile('./lib/Backbone/Graph/lambda/Consumer/.gitignore', ignore)