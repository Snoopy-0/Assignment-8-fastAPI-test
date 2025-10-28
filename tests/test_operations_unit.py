import math
import pytest
from app.operations import add, subtract, multiply, divide

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

def test_subtract():
    assert subtract(10, 3) == 7
    assert subtract(-1, -1) == 0

def test_multiply():
    assert multiply(4, 2.5) == 10.0
    assert multiply(0, 999) == 0

def test_divide_normal():
    assert divide(10, 2) == 5
    assert math.isclose(divide(7, 3), 7/3)

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(1, 0)