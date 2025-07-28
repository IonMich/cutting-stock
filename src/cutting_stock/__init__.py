"""Cutting stock problem solver using CVXPY."""

from .solver import solve, find_combinations, get_max_decimal_places
from .visualization import create_stock_visualization, display_output

__version__ = "0.1.0"
__all__ = ["solve", "find_combinations", "get_max_decimal_places", "create_stock_visualization", "main"]


def main():
    """Main entry point for the cutting stock solver."""
    import argparse
    import numpy as np

    # Default data
    roll_length = 12
    lengths = np.array([3.4, 3.0, 2.7])
    q = np.array([34, 13, 5])

    parser = argparse.ArgumentParser(description='Solve the cutting stock problem using CVXPY')
    parser.add_argument('-r', '--roll_length', type=float, default=roll_length, 
                       help='The length of the stock material. E.g. -r 12.0')
    parser.add_argument('-l', '--lengths', type=float, nargs='+', default=lengths, 
                       help='The lengths of the items. Must be a list of floats. E.g. -l 3.4 3.0 2.7')
    parser.add_argument('-q', '--quantities', type=float, nargs='+', default=q, 
                       help='The quantities of the items. Must be a list of floats. E.g. -q 34 13 5')
    parser.add_argument('-s', '--solver', type=str, default='GLPK', 
                       help='The solver to use. Must be either GLPK or ECOS. E.g. -s GLPK')
    parser.add_argument('-g', '--ge_required', action='store_true', 
                       help='If specified, the constraint is >= instead of ==.')
    parser.add_argument('-v', '--verbose', action='store_true', 
                       help='Show detailed output with input specifications and optimization summary.')
    
    args = parser.parse_args()

    if len(args.lengths) != len(args.quantities):
        raise Exception('Must have the same number of lengths and quantities.')

    # find the max number of decimal places in the lengths
    max_decimal_places = get_max_decimal_places(args.lengths, args.roll_length)

    # Solve the optimization problem
    result = solve(
        lengths=np.array(args.lengths),
        q=np.array(args.quantities),
        roll_length=args.roll_length,
        max_decimal_places=max_decimal_places,
        solver=args.solver,
        ge_required=args.ge_required
    )
    
    # Display the results
    display_output(
        lengths=result['lengths'],
        q=result['q'],
        roll_length=result['roll_length'],
        status=result['status'],
        x_value=result['x_value'],
        objective_value=result['objective_value'],
        A=result['A'],
        c=result['c'],
        max_decimal_places=result['max_decimal_places'],
        verbose=args.verbose
    )