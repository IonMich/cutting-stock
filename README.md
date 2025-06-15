# Cutting Stock Problem

This is a Python implementation of the cutting stock problem.

The problem is described here: https://en.wikipedia.org/wiki/Cutting_stock_problem

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for fast Python package management. If you don't have uv installed, you can install it with:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or on macOS with Homebrew:

```bash
brew install uv
```

### Setup Development Environment

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd cutting_stock
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   uv sync
   ```

3. Activate the virtual environment:
   ```bash
   source .venv/bin/activate  # On Unix/macOS
   # or
   .venv\Scripts\activate     # On Windows
   ```

Alternatively, you can run commands directly with uv without activating the environment:
```bash
uv run python cutting_stock.py
```

## Usage

Basic usage with default input values:

```bash
uv run python cutting_stock.py
```

### Command Line Options

```
-r, --roll_length: The length of the roll. E.g. -r 12.0
-l, --lengths: The lengths of the items. Must be a list of floats. E.g. -l 3.4 3.0 2.7
-q, --quantities: The quantities of the items. Must be a list of floats. E.g. -q 34 13 5
-s, --solver: The solver to use. Must be either GLPK or ECOS. E.g. -s GLPK
-g, --ge_required: If specified, the constraint is >= instead of ==.
```

### Example

```bash
uv run python cutting_stock.py -r 12.0 -l 3.4 3.0 2.7 -q 34 13 5
```

This produces the following output:

```text
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

## Development

### Running Tests

```bash
uv run pytest
```

### Code Formatting

This project uses Black for code formatting and isort for import sorting:

```bash
uv run black .
uv run isort .
```

### Linting

```bash
uv run flake8 .
```

## Dependencies

- **scipy**: Scientific computing library
- **numpy**: Numerical computing library  
- **matplotlib**: Plotting library
- **cvxpy**: Convex optimization library
- **cvxopt**: Convex optimization library

## License

MIT License
