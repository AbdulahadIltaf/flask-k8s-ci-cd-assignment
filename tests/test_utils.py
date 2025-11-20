"""
Unit tests for utility functions.
Tests mathematical operations to ensure correctness.
"""
import sys
import os

# Add parent directory to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utils import add_numbers, multiply_numbers


def test_add_numbers_positive():
    """Test addition with positive integers."""
    assert add_numbers(2, 3) == 5


def test_add_numbers_negative():
    """Test addition with negative and positive integers."""
    assert add_numbers(-1, 1) == 0


def test_add_numbers_zero():
    """Test addition with zero values."""
    assert add_numbers(0, 0) == 0


def test_multiply_numbers_positive():
    """Test multiplication with positive integers."""
    assert multiply_numbers(2, 3) == 6


def test_multiply_numbers_negative():
    """Test multiplication with negative integers."""
    assert multiply_numbers(-1, 5) == -5


def test_multiply_numbers_zero():
    """Test multiplication with zero."""
    assert multiply_numbers(0, 10) == 0