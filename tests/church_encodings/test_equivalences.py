from pytest import mark

from church_encodings.equivalences import to_bool, from_bool, to_int, to_list, from_list, from_pair, to_pair, from_int


@mark.parametrize("b", [True, False])
def test_bool(b):
    assert to_bool(from_bool(b)) == b


@mark.parametrize("p", [(2, 4), (True, False)])
def test_pair(p):
    assert to_pair(from_pair(p)) == p


@mark.parametrize("n", [0, 2, 5, 10])
def test_int(n):
    assert to_int(from_int(n)) == n


@mark.parametrize("l", [[1, 2, 3, 7, 9], [], ["blib", "blob"]])
def test_list(l):
    assert to_list(from_list(l)) == l



