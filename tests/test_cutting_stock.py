"""
Test cases for the cutting stock problem solver.
"""
import numpy as np
import pytest

from src.cutting_stock import find_combinations, get_max_decimal_places, solve


def test_get_max_decimal_places():
    """Test the get_max_decimal_places function."""
    lengths = [3.4, 3.0, 2.7]
    roll_length = 12.0
    result = get_max_decimal_places(lengths, roll_length)
    assert result == 1
    
    # Test with integer roll length
    result = get_max_decimal_places(lengths, 12)
    assert result == 1


def test_find_combinations():
    """Test the find_combinations function."""
    lengths = [3.4, 3.0, 2.7]
    roll_length = 12.0
    max_decimal_places = 1
    
    a_ij, c_i = find_combinations(lengths, roll_length, max_decimal_places)
    
    # Should have some combinations
    assert len(a_ij) > 0
    assert len(c_i) > 0
    assert len(a_ij) == len(c_i)
    
    # Each pattern should use the correct number of item types
    for pattern in a_ij:
        assert len(pattern) == len(lengths)
        assert all(count >= 0 for count in pattern)


def test_solve_basic():
    """Test the solve function with basic inputs."""
    lengths = np.array([3.4, 3.0, 2.7])
    quantities = np.array([34, 13, 5])
    roll_length = 12.0
    max_decimal_places = 1
    
    result = solve(
        lengths=lengths,
        q=quantities,
        roll_length=roll_length,
        max_decimal_places=max_decimal_places,
        solver='GLPK'
    )
    
    # Should return a dictionary with solution data
    assert result is not None
    assert isinstance(result, dict)
    assert 'status' in result
    assert 'x_value' in result
    assert 'objective_value' in result
    
    # If optimal, should have a valid solution
    if result['status'] == 'optimal':
        assert result['x_value'] is not None
        assert all(val >= 0 for val in result['x_value'])


def test_solve_ge_constraint():
    """Test the solve function with >= constraint."""
    lengths = np.array([3.4, 3.0, 2.7])
    quantities = np.array([34, 13, 5])
    roll_length = 12.0
    max_decimal_places = 1
    
    result = solve(
        lengths=lengths,
        q=quantities,
        roll_length=roll_length,
        max_decimal_places=max_decimal_places,
        solver='GLPK',
        ge_required=True
    )
    
    # Should return a dictionary with solution data
    assert result is not None
    assert isinstance(result, dict)
    assert 'status' in result


def test_solve_invalid_solver():
    """Test that invalid solver raises an exception."""
    lengths = np.array([3.4, 3.0, 2.7])
    quantities = np.array([34, 13, 5])
    roll_length = 12.0
    max_decimal_places = 1
    
    with pytest.raises(Exception, match="Invalid solver"):
        solve(
            lengths=lengths,
            q=quantities,
            roll_length=roll_length,
            max_decimal_places=max_decimal_places,
            solver='INVALID'
        )
