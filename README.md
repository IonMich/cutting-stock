# Cutting Stock Problem

This is a Python implementation of the cutting stock problem.

The problem is described here: https://en.wikipedia.org/wiki/Cutting_stock_problem

# Installations

To install the required packages using `pip` in your current environment, run:

`pip install -e .`

To create a new `conda` environment with all the required packages, run:

```
conda env create --file environment.yml --name cvx-py310
conda activate cvx-py310
```

# Usage

Basic usage with default input values:

`python cutting_stock.py`

Options:

```
-r, --roll_length: The length of the roll. E.g. -r 12.0
-l, --lengths: The lengths of the items. Must be a list of floats. E.g. -l 3.4 3.0 2.7
-q, --quantities: The quantities of the items. Must be a list of floats. E.g. -q 34 13 5
-s, --solver: The solver to use. Must be either GLPK or ECOS. E.g. -s GLPK
-g, --ge_required: If specified, the constraint is >= instead of ==.
```

For example:

`python cutting_stock.py -r 12.0 -l 3.4 3.0 2.7 -q 34 13 5`

which produces the following output:

```
Input data:
lengths = [3.4 3.  2.7]
Quantities = [34 13  5]
Roll length = 12
Derived max decimal places = 1
lower bound for number of patterns:  14.008333333333333 , i.e. after rounding:  15.0
status: optimal
optimal value of fyra 23.9 m
optimal var [ 0.  0.  0.  0.  0.  0.  0.  0.  0. 10.  0.  2.  0.  0.  0.  0.  0.  0.
  0.  0.  0.  3.  0.  0.  1.  0.]

============================
========= PATTERNS =========
============================

total number of rolls used: 16 

pattern 9 used 10 times, cost 1.8 total cost 18.0
this pattern is:
        item with length 3.4 m used 3 times
        item with length 3.0 m used 0 times
        item with length 2.7 m used 0 times


pattern 11 used 2 times, cost 2.5 total cost 5.0
this pattern is:
        item with length 3.4 m used 2 times
        item with length 3.0 m used 0 times
        item with length 2.7 m used 1 times


pattern 21 used 3 times, cost 0.0 total cost 0.0
this pattern is:
        item with length 3.4 m used 0 times
        item with length 3.0 m used 4 times
        item with length 2.7 m used 0 times


pattern 24 used 1 times, cost 0.9 total cost 0.9
this pattern is:
        item with length 3.4 m used 0 times
        item with length 3.0 m used 1 times
        item with length 2.7 m used 3 times
```
