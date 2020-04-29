#!/usr/bin/env python
import json
import os

# load keywords to dictionary
keywords={}
with open('keywords.json') as j_file:
    keywords = json.load(j_file)

# output the keyword when value is given
def getKey(v):
    for key, value in keywords.items():
        if(v in value):
            print (key, v)

# open the solution
def openSolution():
    cur_path = os.getcwd()
    solution = open(cur_path+"/solutions/a/main.c", "r")
    return solution.read()

# replace operators,semicolons, etc..
def cleanCode(s):
    r = [';','+','=','/','*','-','[',']','(',')','"',':','{','}','//','#','<','>','\n',]
    for i in r:
        s = s.replace(i,' ')

    s = s.replace("'","")
    return s

# split the code into words
def splitCode(s):
    w = s.split(" ")
    return w

# print tree
def printTree(s):
    for i in s:
        getKey(i)

# main
fileText = openSolution()
newFile = cleanCode(fileText)
printTree(splitCode(newFile))
