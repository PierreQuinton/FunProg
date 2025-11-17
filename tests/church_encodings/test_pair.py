from pytest import mark

from church_encodings import p_pair, p_first, p_second, b_true, b_false


@mark.parametrize("a", [2, "yep", [3, 4, 6]])
@mark.parametrize("b", [5, "nope", [2, 7]])
def test_pair(a, b):
    p = p_pair(a, b)

    assert p(b_true) == a
    assert p(b_false) == b


@mark.parametrize("a", [2, "yep", [3, 4, 6]])
@mark.parametrize("b", [5, "nope", [2, 7]])
def test_first(a, b):
    p = p_pair(a, b)

    assert p_first(p) == a


@mark.parametrize("a", [2, "yep", [3, 4, 6]])
@mark.parametrize("b", [5, "nope", [2, 7]])
def test_first(a, b):
    p = p_pair(a, b)

    assert p_second(p) == b
