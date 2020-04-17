#!/usr/bin/env python

# autochecker
# tailored to C source files in the format submissions/studentid/studentid.c
# tests should be provided as tests/testfile.in, tests/testfile.out

# for each submission, compiles and runs the source against a set of test inputs
# compares the program output to expected output and calculates marks
# marks are added for compilation and correctly passing each test

# usage: ./autocheck.py --dir=<submission-dir> --test=<tests-dir>
#             --marks=<marks for compilation>,<marks per testcase> [--no-color] [--no-run] [--summary]
# example: ./autocheck.py --dir=submissions --test=tests --marks=40,5 --summary

# TODO: seperate code into modules
# TODO: seperate UI from logic - i.e. first process the files then decide printing based on flags

import os
import sys
import re
import collections
from subprocess import Popen, call, PIPE

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def green(s):
    global colors
    if colors:
        return bcolors.OKGREEN + s + bcolors.ENDC
    else:
        return s

def blue(s):
    global colors
    if colors:
        return bcolors.OKBLUE + s + bcolors.ENDC
    else:
        return s

def red(s):
    global colors
    if colors:
        return bcolors.FAIL + s + bcolors.ENDC
    else:
        return s

def orange(s):
    global colors
    if colors:
        return bcolors.WARNING + s + bcolors.ENDC
    else:
        return s

def bold(s):
    global colors
    if colors:
        return bcolors.BOLD + s + bcolors.ENDC
    else:
        return s

def lenformat(s):
    global flen
    s1 = '{0:'+str(flen)+'}'
    s1 = s1.format(s)
    return s1

def prep_tests():
    global testdir, test_in, test_out, home, run, summary
    if run:
        test_in = {}
        test_out = {}
        os.chdir(testdir)

        for testfile in os.listdir('.'):
            fname = testfile.split('.')[0]
            fext = testfile.split('.')[1]
            file = open(testfile,'r')

            global flen
            flen = max(flen, len(fname))

            if fext == 'in':
                test_in[fname] = file.read().strip()
            elif fext == 'out':
                test_out[fname] = file.read().strip()

        os.chdir(home)
        test_in = collections.OrderedDict(sorted(test_in.items()))

        for key in test_in.keys():
            if not summary:
                print 'LOADING', lenformat(key), '-', repr(test_in[key]), ':', repr(test_out[key])
            global tpass
            tpass += 1

        if summary:
            print tpass, 'tests loaded successfully'
    else:
        print 'Runtime tests not loaded for --no-run'

def compare(test, expected, result):
    matchlist = re.findall('\d+\.\d{2}', result)
    stest = lenformat(test)
    global summary

    if len(matchlist)==0:
        if not summary:
            print '    ', stest, '-', red('FAIL'), ' : unexpected format'
    else:
        result = matchlist[-1]
        if result == expected:
            global cpass, marks, tmarks
            marks += tmarks
            cpass += 1
            if not summary:
                print '    ', stest, '-', green('PASS')
        else:
            if not summary:
                print '    ', stest, '-', red('FAIL'), ': expected {0} returned {1}'.format(expected, result)

def run_file(filepath, studentid):
    global cpass, npass, tpass
    cpass = 0
    for key in test_in.keys():
        p = Popen(['./a.out'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        result = p.communicate(test_in[key])[0]
        compare(key, test_out[key], result)
    if cpass == tpass:
        npass += 1

def compile_file(filepath, studentid):
    f = open('compile.out', 'w')
    r = call(['gcc', filepath], stdout=f, stderr=f)
    f.close()
    if os.path.exists('a.out'):
        global csuccess, marks, cmarks, summary, run
        marks += cmarks
        csuccess += 1
        os.remove('compile.out')

        if not summary:
            print '    ', blue('Compile'), green('OK')
        elif not run:
            print blue('Compile'), green('OK')

        if run:
            run_file(filepath, studentid)
    else:
        global cfail
        cfail += 1
        if not summary:
            print '    ',
        print blue('Compile'), red('FAIL')

def process_file(filepath):
    global marks, summary, run
    marks = 0
    a = filepath.split('/')
    studentid = a[len(a)-2]
    if summary:
        print studentid,
    else:
        print orange(studentid)
    compile_file(filepath, studentid)
    if summary:
        if run and marks!=0:
            print blue('Compile'), green('OK') + ' ' + orange('marks ='), bold(green(str(marks)))
    else:
        if marks!=0:
            print '     marks =', bold(green(str(marks)))

def process(cur):
    global ext, count
    if os.path.isfile(cur):
        #if (ext==None or cur.endswith(ext)):
        if cur.endswith('.c'):
            filepath = os.path.abspath(cur)
            process_file(filepath)
            global count
            count += 1
    else:
        os.chdir(cur)
        for dir in os.listdir('.'):
            process(dir)
        os.chdir('..')

def parse_args():
    global ext, stdir, testdir, colors, summary, run

    for arg in sys.argv:
        if arg.startswith('--dir'):
            stdir = arg.split('=')[1]
        elif arg.startswith('--test'):
            testdir = arg.split('=')[1]
        elif arg.startswith('--no-color'):
            colors = False
        elif arg.startswith('--marks'):
            cmarks = arg.split('=')[1].split(',')[0]
            tmarks = arg.split('=')[1].split(',')[1]
        elif arg.startswith('--summary'):
            summary = True
        elif arg.startswith('--no-run'):
            run = False
            summary = True

def init():
    global csuccess, cfail, ext, stdir, testdir, count, flen, colors, cpass
    global tpass, npass, home, cmarks, tmarks, summary, run
    home = os.getcwd()  # current working directory
    csuccess = 0        # how many successful compilations
    cfail = 0           # how many failed compilations
    count = 0           # total number of submissions
    cpass = 0           # how many test cases passed
    tpass = 0           # how many test cases in total
    npass = 0           # how many students passed all tests
    testdir = '.'       # test directory
    stdir = '.'         # submission directory
    flen = 0            # maximum length of test name - for formatting purposes
    colors = True       # if colors are on/off - formatting only
    cmarks = 40         # marks for compilation
    tmarks = 5          # marks per test
    summary = False     # show summaries only
    run = True          # run after compiling

def print_loading_tests():
    print '\n----------- Loading Tests -------------\n'

def print_start_message():
    print '\n----------- Starting Autochecker -------------\n'

def print_results():
    print '\n----------- Autochecking Complete  ------------\n'
    print 'TOTAL: {0}'.format(count)
    print 'COMPILED: {0}'.format(csuccess)
    print 'COMPILE FAILED: {0}'.format(cfail)

    global run
    if run:
        print 'ALL TESTS PASSED: {0}'.format(npass)
    print ''

def main():
    init()
    parse_args()
    print_loading_tests()
    prep_tests()
    print_start_message()
    process(stdir)
    print_results()

if __name__ == "__main__":
    main()
