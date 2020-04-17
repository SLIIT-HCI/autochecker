import os
import sys

if len(sys.argv)<=1:
    print 'You must specify a folder'
    exit(1)

os.chdir(sys.argv[1])
for sub in os.listdir('.'):
    if os.path.isdir(sub):
        os.chdir(sub)
        for file in os.listdir('.'):
            print os.path.abspath(file)
        os.chdir('..')
