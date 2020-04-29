# autochecker
autochecker is a tool written for autograding programming assignments using blackbox testing. The idea is to run a set of tests (inputs, expected outputs) against each student submission and provide marks based on the results.

## Getting Started

### Prerequisites
* Python 2.7 - [https://www.python.org/downloads/release/python-2718/](https://www.python.org/downloads/release/python-2718/)

### Setting Up
* Clone this repository to a suitable location e.g.`~/autocheck`
* Copy the tests into a folder e.g. `~/autocheck/tests`

	> Some tests have been provided that could be edited for requirement. See section below for test guidelines

* Copy your student submissions into a folder e.g. `~/autocheck/submissions`

	> submissions should be in the format of  `<student-id>/<source-files>` e.g. `~/autocheck/submissions/IT120019180/main.c`

### Creating Tests
* Tests are provided as pairs: `filename.in` and `filename.out`
* The `.in` file contains the sample input that will be piped into the standard input when the program runs
* The `.out` file contains the expected output that will be checked against the generated output from the student submission
* Tests will be executed in lexicographic order of filenames

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

## Best Practices
These best practices are listed from previous experience and extensive trial and error.

* Prepare the programming assignment to be compatible for autochecker use
	* Require students to adhere to a strict input/output format from stdin/out or files
	* Provide students with a written example of the input/output format, or provide a skeleton code to get started
	* Provide students with some sample inputs and outputs used by autochecker
	* Vet the assignment spec, sample solution and tests before publishing to students

* Provide students access to autochecker with a subset of tests used for marking. Alternatively you could have separate sets of _public_ and _private_ tests for use by students and staff respectively

* Encourage incremental development of solutions. I.e. At every step, encourage students to compile/run/test their code to ensure they are free of compile and runtime errors, and they comply with the provided _public tests_

* You could test a programs various functions and use of programming concepts by writing different tests to target a program's different execution paths. Use principles from Unit Testing (tests should be isolated, automated, atomic, etc.) and Unit Test coverage for best results.

## Credits
This tool is inspired by [https://github.com/ChrisJefferson/stacscheck](https://github.com/ChrisJefferson/stacscheck)
