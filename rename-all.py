# renames the student submission folders to the following format
# submissions/studentid/source.c

# usage: python list-all.py <directory>
# example: python list-all.py submissions

import os
import sys

if len(sys.argv)<=1:
    print 'You must specify a folder'
    exit(1)

os.chdir(sys.argv[1])

for sub in os.listdir('.'):
    if os.path.isdir(sub):
        index = sub.find(' ')
        if index != -1:
            sub_dir = sub[0:index]
            os.rename(sub, sub_dir)
            print(sub_dir)
            """
            os.chdir(sub_dir)
            if not os.path.exists('source'):
                os.mkdir('source')
                print('    source created')
            for sub_file in os.listdir('.'):
                if os.path.isfile(sub_file):
                    os.rename(sub_file, 'source/'+sub_file)
                    print('    ' + sub_file)
            os.chdir('..')
            """
