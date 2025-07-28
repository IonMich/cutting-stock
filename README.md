# Cutting Stock Problem

A CVXPY implementation of the [cutting-stock problem](https://en.wikipedia.org/wiki/Cutting_stock_problem).

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for fast Python package management. If you don't have uv installed, you can install it with:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Setup Development Environment

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd cutting-stock
   ```

2. You can run commands directly with uv without activating the environment or manually installing dependencies:

   ```bash
   uv run cutting-stock
   ```

## Command Line Options

``` console
-r, --roll_length: The length of the roll. E.g. -r 12.0
-l, --lengths: The lengths of the items. Must be a list of floats. E.g. -l 3.4 3.0 2.7
-q, --quantities: The quantities of the items. Must be a list of floats. E.g. -q 34 13 5
-s, --solver: The solver to use. Must be either GLPK or ECOS. E.g. -s GLPK
-g, --ge_required: If specified, the constraint is >= instead of ==.
--verbose: If specified, the output will be more verbose.
```

### Example

```bash
uv run cutting-stock -r 12.0 -l 3.4 3.0 2.7 -q 34 13 5
```

This produces the following output:

```console
> uv run cutting-stock
Required pieces:
███ 3.4m ×34   ▓▓▓ 3.0m ×13   ▒▒▒ 2.7m ×5
Stock length: 12m

Solution: 16 stocks of 12m each, 23.9m waste

Use 10× → 3.4m |3.4m |3.4m |1.8m
          █████|█████|█████|···· (12m stock)
Use  2× → 3.4m |3.4m |2.7m|2.5m
          █████|█████|▒▒▒▒|···· (12m stock)
Use  3× → 3.0m |3.0m |3.0m |3.0m 
          ▓▓▓▓▓|▓▓▓▓▓|▓▓▓▓▓|▓▓▓▓▓ (12m stock)
Use  1× → 3.0m |2.7m|2.7m|2.7m|0.9m
          ▓▓▓▓▓|▒▒▒▒|▒▒▒▒|▒▒▒▒|···· (12m stock)
```

## Development

### Running Tests

```bash
uv run pytest
```

### Code Formatting and Linting

```bash
uv run ruff check src/
```

## Dependencies

- **scipy**: Scientific computing library
- **numpy**: Numerical computing library
- **cvxpy**: Convex optimization library
- **cvxopt**: Convex optimization library

## License

MIT License
