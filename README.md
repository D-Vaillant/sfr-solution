# surface-routing-problem.py

A symbolic solution to a particularly simple case of the surface routing problem.

Details of the surface routing problem are found in `simple_case.case_description`.


## Usage

There are two ways to use this script: either install it using pip or just run the script from the command-line directly.

### Installation

Clone this repo and navigate to the directory. You can either do:

`pip install .`

to install it to your global Python library, or you do:

`virtualenv env`

`activate` (if it isn't activated already)

`pip install .`

in order to install it to a cloistered version of Python. Help can be obtained by using:

`solve_case -h`


### Script

Just do:

`python simple_case.py HEIGHT WIDTH REGION_ROT LINE_ROT`

Make sure that you have sympy installed.
