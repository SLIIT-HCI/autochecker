import os
import sys
import re

if len(sys.argv)<=1:
    print 'You must specify a folder'
    exit(1)

os.chdir(sys.argv[1])

for sub in os.listdir('.'):
    os.chdir(sub)
    c = '.'
    for file in os.listdir('.'):
        if (file.endswith('.c')):
            f = open(file, 'r')
            code = f.read()
            if re.search('loyalty', code, re.IGNORECASE):
                c = 'a'
                print sub, '----- A'
            elif re.search('salary', code, re.IGNORECASE):
                c = 'b'
                print sub, '-- B'
            else:
                print sub, 'uncategorised'
            break
    os.chdir('..')

    if len(sys.argv)==2 and sys.argv[1]=='--move':
        os.rename(sub, c+'/'+sub)
