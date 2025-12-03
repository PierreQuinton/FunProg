from pytest import mark

from church_encodings.equivalences import to_option, from_option, from_bool
from church_encodings.option import o_none, o_some, o_is_none, o_get_or_else, o_is_some, o_map, \
    o_flatmap


def test_none():
    assert to_option(o_none) is None


@mark.parametrize("x", [2, "abc", [3, 4, 5], None])
def test_some(x):
    assert to_option(o_some(x)) == x


@mark.parametrize("o", [0, None, [None], 1, 2])
def test_is_none(o):
    o_o = from_option(o)
    assert o_is_none(o_o) == from_bool(o is None)

@mark.parametrize("o", [0, None, [None], 1, 2])
def test_is_some(o):
    o_o = from_option(o)
    assert o_is_some(o_o) == from_bool(o is not None)


@mark.parametrize("o", [0, None, [None], 1, 2])
@mark.parametrize("y", [0, None, [None], 1, 2])
def test_get_or_else(o, y):
    o_o = from_option(o)
    assert o_get_or_else(o_o, y) == (o if o is not None else y)


@mark.parametrize("o", [0, None, 1, 2])
def test_map(o):
    o_o = from_option(o)
    assert to_option(o_map(o_o, lambda x: x+1)) == (o+1 if o is not None else None)


@mark.parametrize("o", [0, None, 1, 2, 3])
def test_flatmap(o):
    g = lambda x: (o_some(x + 1) if x % 2 == 0 else o_none)
    o_o = from_option(o)
    assert to_option(o_flatmap(o_o, g)) == (to_option(g(o)) if o is not None else None)
