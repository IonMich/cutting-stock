# solve the cutting stock problem
# using cvxpy

# Notation:
# q_j = quantity required of item j
# c_i = cost of pattern i
# a_ij = amount of item j in pattern i
# x_i = number of patterns i used

import cvxpy as cp
import numpy as np
from typing import List, Tuple


# first find a_ij and c_i for all possible combinations that fit in the roll
# note that we have an unlimited supply of each item, so we can use as much as we want.
def find_combinations(lengths: List[float], roll_length: float, max_decimal_places: int) -> Tuple[List[List[int]], List[float]]:
    
    # find all combinations of lengths
    from itertools import combinations_with_replacement
    max_combination_length = int(roll_length / min(lengths))
    combinations: List[Tuple[float, ...]] = []
    for i in range(1, max_combination_length + 1):
        combinations += list(combinations_with_replacement(lengths, i))

    # find a_ij and c_i
    a_ij = []
    c_i = []
    for combination in combinations:
        # a valid combination is one where the sum of the lengths is less than the roll length
        if sum(combination) <= roll_length:
            # enumerate the lengths in the combination
            a_ij.append([combination.count(length) for length in lengths])
            cost = roll_length - sum(combination)
            # round the cost to the max number of decimal places in the lengths
            c_i.append(round(cost, max_decimal_places))

    return a_ij, c_i

def solve(lengths, q, roll_length, max_decimal_places, silent=False, solver='GLPK', ge_required=False):

    a_ij, c = find_combinations(lengths, roll_length, max_decimal_places)
    A = np.array(a_ij).T

    # define the cvxpy problem using the mixed integer 
    # linear programming solver
    x = cp.Variable(len(c), integer=True)
    objective = cp.Minimize(cp.sum(cp.multiply(c, x)))
    if ge_required:
        constraints = [A @ x >= q]
    else:
        constraints = [A @ x == q]
    constraints += [x >= 0]
    prob = cp.Problem(objective, constraints)

    # solve the problem
    if solver == 'GLPK':
        prob.solve(solver=cp.GLPK_MI)
    elif solver == 'ECOS':
        prob.solve(solver=cp.ECOS)
    else:
        raise Exception('Invalid solver, must be ECOS or GLPK.')

    if not silent:
        # input data
        print('Input data:')
        print('lengths =', lengths)
        print('Quantities =', q)
        print('Roll length =', roll_length)
        print('Derived max decimal places =', max_decimal_places)
        # note that the lower bound for the number of patterns is the total length of the items required
        # divided by the roll length
        print('lower bound for number of patterns: ', (lengths @ q) / roll_length, ", i.e. after rounding: ", np.ceil((lengths @ q) / roll_length))

        # print the results
        print("status:", prob.status)
        print("optimal value of fyra", prob.value, "m")
        print("optimal var", x.value)
        # print the number of each pattern used, the cost of each pattern, and finally the total cost
        if prob.status == 'optimal' and x.value is not None:
            
            print('\n============================')
            print('========= PATTERNS =========')
            print('============================\n')
            print("total number of rolls used:", round(sum(x.value)), "\n")
            for i in range(len(c)):
                # only print the patterns that are used
                if x.value[i] > 0:
                    print("pattern", i, "used", round(float(x.value[i])), "times, cost", c[i], "total cost", c[i] * round(float(x.value[i])))
                    print("this pattern is:")
                    for j in range(len(q)):
                        print("\titem with length", lengths[j], "m used", A[j][i], "times")
                    print("\n")

    return x.value


def get_max_decimal_places(lengths: List[float], roll_length: float) -> int:
    max_decimal_places = max([len(str(length).split('.')[1]) if '.' in str(length) else 0 for length in lengths])
    if isinstance(roll_length, float) and '.' in str(roll_length):
        max_decimal_places = max(max_decimal_places, len(str(roll_length).split('.')[1]))
    return max_decimal_places

def main():
    """Main entry point for the cutting stock solver."""
    import argparse

    # Default data
    roll_length = 12
    lengths = np.array([3.4, 3.0, 2.7])
    q = np.array([34, 13, 5])

    parser = argparse.ArgumentParser(description='Solve the cutting stock problem using CVXPY')
    parser.add_argument('-r', '--roll_length', type=float, default=roll_length, help='The length of the roll. E.g. -r 12.0')
    parser.add_argument('-l', '--lengths', type=float, nargs='+', default=lengths, help='The lengths of the items. Must be a list of floats. E.g. -l 3.4 3.0 2.7')
    parser.add_argument('-q', '--quantities', type=float, nargs='+', default=q, help='The quantities of the items. Must be a list of floats. E.g. -q 34 13 5')
    parser.add_argument('-s', '--solver', type=str, default='GLPK', help='The solver to use. Must be either GLPK or ECOS. E.g. -s GLPK')
    parser.add_argument('-g', '--ge_required', action='store_true', help='If specified, the constraint is >= instead of ==.')
    args = parser.parse_args()

    if len(args.lengths) != len(args.quantities):
        raise Exception('Must have the same number of lengths and quantities.')

    # find the max number of decimal places in the lengths
    max_decimal_places = get_max_decimal_places(args.lengths, args.roll_length)

    x_solve = solve(
        lengths=np.array(args.lengths),
        q=np.array(args.quantities),
        roll_length=args.roll_length,
        max_decimal_places=max_decimal_places,
        solver=args.solver,
        ge_required=args.ge_required
    )
    return x_solve


if __name__ == "__main__":
    main()

