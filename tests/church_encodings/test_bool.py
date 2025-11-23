from pytest import mark

from church_encodings.bool import b_true, b_false, b_not, b_or, b_and
from church_encodings.equivalences import from_bool


@mark.parametrize("x", [2, "yep", [3, 4, 6]])
@mark.parametrize("y", [5, "nope", [2, 7]])
def test_true(x, y):
    assert b_true(x, y) == x


@mark.parametrize("x", [2, "yep", [3, 4, 6]])
@mark.parametrize("y", [5, "nope", [2, 7]])
def test_false(x, y):
    assert b_false(x, y) == y


@mark.parametrize("b", [True, False])
def test_not(b):
    assert b_not(from_bool(b)) == from_bool(not b)


@mark.parametrize("b1", [True, False])
@mark.parametrize("b2", [True, False])
def test_or(b1, b2):
    assert b_or(from_bool(b1), from_bool(b2)) == from_bool(b1 or b2)


@mark.parametrize("b1", [True, False])
@mark.parametrize("b2", [True, False])
def test_and(b1, b2):
    assert b_and(from_bool(b1), from_bool(b2)) == from_bool(b1 and b2)
