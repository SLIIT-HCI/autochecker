
# autochecker
Autochecker is a tool written for autograding programming assignments using blackbox testing. The idea is to run a set of tests (inputs, expected outputs) against each student submission and provide marks based on the results.

## Getting Started

### Prerequisites
* Python 2.7 - [https://www.python.org/downloads/release/python-2718/](https://www.python.org/downloads/release/python-2718/)

### Setting Up
* Clone this repository to a suitable location e.g.`~/autocheck`
* Copy the tests into a folder e.g. `~/autocheck/tests`

	> See section below on how to create tests
* Copy your student submissions into a folder e.g. `~/autocheck/submissions` 

	> submissions should be in the format of
	> `<student-id>/<source-files>`
	> e.g. `~/autocheck/submissions/IT120019180/main.c`

### Creating Tests
TODO: write this section

### Running
Run the autochecker using the following command:

> `autocheck --tests=<test-folder> --submissions=<submission-folder>`

Use the following additional commands to configure your runtime
* `--marks=x,y`  where x = marks for compilation, y = marks per testcase
ensure that x + y * no_testcases = 100

* `--colors` presents the output in a colourful format
* `--summary` presents the output in a summarised form
* `--no-run` only compiles the code and does not run the test cases
* `--timeout=seconds`provide (in seconds) the time limit per test case 

e.g. `cd ~/autocheck | ./autocheck.py --tests=tests --submissions=submissions`

## Limitations
* Student submissions with the following outcomes must be checked by a human marker
	* Do not compile
	* Times out - e.g. due to getting stuck in infinite loops or additional user inputs
	* Fails all tests - e.g. due to unexpected output format
	
* Only supports blackbox testing - i.e. doesn't analyse source code 
* To be tested, programs must write the output to a file or standard output to be checked, and (optionally) take input from the standard input or files

## Tips
TODO: write this section

## Credits
This tool is inspired by [https://github.com/ChrisJefferson/stacscheck](https://github.com/ChrisJefferson/stacscheck)
