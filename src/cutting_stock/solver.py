"""Core cutting stock problem solver using CVXPY."""

import cvxpy as cp
import numpy as np
from typing import List, Tuple, Dict, Any


def find_combinations(lengths: List[float], roll_length: float, max_decimal_places: int) -> Tuple[List[List[int]], List[float]]:
    """Find all valid combinations of pieces that fit in a stock roll."""
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


def get_max_decimal_places(lengths: List[float], roll_length: float) -> int:
    """Calculate the maximum number of decimal places in the input data."""
    max_decimal_places = max([len(str(length).split('.')[1]) if '.' in str(length) else 0 for length in lengths])
    if isinstance(roll_length, float) and '.' in str(roll_length):
        max_decimal_places = max(max_decimal_places, len(str(roll_length).split('.')[1]))
    return max_decimal_places


def solve(lengths, q, roll_length, max_decimal_places, solver='GLPK', ge_required=False) -> Dict[str, Any]:
    """
    Solve the cutting stock problem using mixed integer linear programming.
    
    Returns a dictionary containing all the solution data needed for output formatting.
    """
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

    # Return all the data needed for visualization
    return {
        'status': prob.status,
        'x_value': x.value,
        'objective_value': prob.value,
        'A': A,
        'c': c,
        'lengths': lengths,
        'q': q,
        'roll_length': roll_length,
        'max_decimal_places': max_decimal_places
    }