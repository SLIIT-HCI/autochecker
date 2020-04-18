#!/usr/bin/env python

# autochecker
# tailored to C source files in the format submissions/studentid/studentid.c
# tests should be provided as tests/testfile.in, tests/testfile.out

# for each submission, compiles and runs the source against a set of test inputs
# compares the program output to expected output and calculates marks
# marks are added for compilation and correctly passing each test

# usage: ./autocheck.py
#               --dir=<submission-dir>  # where the student submission folders are located
#               --test=<tests-dir>      # where the tests are located
#               --marks=<M1>,<M2>       # marks for compilation, marks for running
#               --no-color              # toggle colours in the output
#               --no-run                # if this is set, only compiles, does not run tests
#               --summary               # does not show individual test outcomes
#               --timeout=seconds       # time limit on each test case - to avoid infinite loops

# example: ./autocheck.py --dir=submissions --test=tests --marks=40,5 --no-color --no-run --summary --timeout=0.01

# TODO: seperate code into modules, and cleanup
# TODO: seperate UI from logic - i.e. first process the files then decide printing based on flags
# TODO: add exception handling

from __future__ import division
import os
import sys
import re
import collections
from subprocess import Popen, call, PIPE, STDOUT
from threading import Timer

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
    global summary, all_invalid

    if len(matchlist)==0:
        if not summary:
            print '    ', stest, '-', red('FAIL'), ' : unexpected format'
    else:
        all_invalid = False
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
    global cpass, npass, tpass, timeout, timed_out, all_timeout
    cpass = 0
    for key in test_in.keys():
        timed_out = False
        p = Popen(['./a.out'], stdin=PIPE, stdout=PIPE, stderr=STDOUT)

        def timeout_process():
            global timed_out
            timed_out = True
            p.kill()

        timer = Timer(timeout, timeout_process)
        try:
            timer.start()
            result = p.communicate(test_in[key])[0]
        finally:
            timer.cancel()

        if timed_out:
            if not summary:
                print '    ', lenformat(key), '-', red('FAIL'), ': timed out'
        else:
            all_timeout = False
            compare(key, test_out[key], result)

    if cpass == tpass:
        npass += 1

def compile_file(filepath, studentid):
    f = open('compile.out', 'w')
    r = call(['gcc', filepath], stdout=f, stderr=f)
    f.close()
    if os.path.exists('a.out'):
        global csuccess, marks, cmarks, summary, run, all_invalid, all_timeout, ctimeout, cinvalid
        marks += cmarks
        csuccess += 1
        os.remove('compile.out')

        if not summary:
            print '    ', blue('Compile'), green('OK')
        elif not run:
            print blue('Compile'), green('OK')

        if run:
            all_timeout = True
            all_invalid = True
            run_file(filepath, studentid)
            if all_invalid:
                cinvalid += 1
            if all_timeout:
                ctimeout += 1
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
            print blue('Compile'), green('OK'),
            if all_timeout:
                print '- all tests timed out'
            elif all_invalid:
                print '- all outputs in unexpected format'
            else:
                print orange('marks ='), bold(green(str(marks)))
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
    global ext, stdir, testdir, colors, summary, run, timeout

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
        elif (arg.startswith('--timeout')):
            timeout = float(arg.split('=')[1])

def init():
    global csuccess, cfail, ext, stdir, testdir, count, flen, colors, cpass
    global tpass, npass, home, cmarks, tmarks, summary, run, timeout
    global ctimeout, cinvalid
    home = os.getcwd()  # current working directory
    csuccess = 0        # how many successful compilations
    ctimeout = 0        # how many submissions timed out
    cinvalid = 0        # how many submissions had invalid output format
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
    timeout = 0.01      # timeout 10 milliseconds

def print_loading_tests():
    print '\n----------- Loading Tests -------------\n'

def print_start_message():
    print '\n----------- Starting Autochecker -------------\n'

def p(c):
    global count
    return c * 100 / count

def print_results():
    print '\n----------- Autochecking Complete  ------------\n'
    print 'TOTAL SUBMISSIONS: {0:>4}'.format(count)
    print ''
    print 'COMPILE FAILED:    {0:>4} ( {1:>2.2f} % )'.format(cfail, p(cfail))

    global run, cinvalid, ctimeout
    if run:
        ceval = csuccess - ctimeout - cinvalid
        print 'TIMED OUT:         {0:>4} ( {1:>2.2f} % )'.format(ctimeout, p(ctimeout))
        print 'INVALID OUTPUT:    {0:>4} ( {1:>2.2f} % )'.format(cinvalid, p(cinvalid))
        print ''
        print 'EVALUATED:         {0:>4} ( {1:>2.2f} % )'.format(ceval, p(ceval))
    else:
        print 'COMPILE SUCESSFUL: {0:>4} ( {1:>2.2f} % )'.format(csuccess, p(csuccess))
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
