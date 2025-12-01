from pytest import mark

from church_encodings.list import l_nil, l_cons, l_append, l_is_nil, l_is_non_empty, l_head, l_tail, l_filter, l_map, l_flat_map, l_at
from church_encodings.equivalences import  from_list, to_list, from_bool, to_bool, from_int


def test_nil():
    assert to_list(l_nil) == []


@mark.parametrize("h", [2, "blab"])
@mark.parametrize("l", [[], [1, 2, 3], ["blob", "blib", "bloub"]])
def test_cons(h, l):
    assert to_list(l_cons(h, from_list(l))) == [h] + l


@mark.parametrize("l1", [[], [7, 8, 2], ["blub", "bleb", "bloinb"]])
@mark.parametrize("l2", [[], [1, 2, 3], ["blob", "blib", "bloub"]])
def test_append(l1, l2):
    assert to_list(l_append(from_list(l1), from_list(l2))) == l1 + l2


@mark.parametrize("l", [[], [1, 2, 3], ["blob", "blib", "bloub"]])
def test_is_nil(l):
    assert to_bool(l_is_nil(from_list(l))) == (len(l) == 0)


@mark.parametrize("l", [[], [1, 2, 3], ["blob", "blib", "bloub"]])
def test_is_non_empty(l):
    assert to_bool(l_is_non_empty(from_list(l))) == (len(l) != 0)


@mark.parametrize("l", [[1], [1, 2, 3], ["blob", "blib", "bloub"]])
def test_head(l):
    assert l_head(from_list(l)) == l[0]


@mark.parametrize("l", [[1], [1, 2, 3], ["blob", "blib", "bloub"]])
def test_tail(l):
    assert to_list(l_tail(from_list(l))) == l[1:]


@mark.parametrize("l", [[1], [3, 2, 9], [1, 6, 9, 3]])
@mark.parametrize("p", [lambda x: x % 3 == 0, lambda x: x <= 3])
def test_filter(l, p):
    fromed_p = lambda x: from_bool(p(x))
    fromed_l = from_list(l)
    assert to_list(l_filter(fromed_l, fromed_p)) == [x for x in l if p(x)]


@mark.parametrize("l", [[1], [3, 2, 9], [1, 6, 9, 3]])
@mark.parametrize("f", [lambda x: x % 3, lambda x: x ** 2])
def test_map(l, f):
    fromed_l = from_list(l)
    assert to_list(l_map(fromed_l, f)) == [f(x) for x in l]

@mark.parametrize("ls", [
    [[1], [3, 2, 9], [1, 6, 9, 3]],
    [["blab"], [], ["bloub", "blob"]]
])
def test_flat_map(ls):
    fromed_ls = from_list([from_list(l) for l in ls])
    assert to_list(l_flat_map(fromed_ls)) == [a for l in ls for a in l]
