from church_encodings.bool import b_false, b_true
from church_encodings.option import o_some, o_none
from church_encodings.pair import p_pair, p_first, p_second
from church_encodings.int import  i_zero, i_succ
from church_encodings.list import l_nil, l_cons


def from_bool(b):
    return b_true if b else b_false


def to_bool(b):
    return b(True, False)


def from_pair(p):
    x, y = p
    return p_pair(x, y)


def to_pair(p):
    return (p_first(p), p_second(p))


def from_int(n):
    temp = i_zero
    for i in range(n):
        temp = i_succ(temp)

    return temp


def to_int(n):
    return n(lambda x: x+1, 0)


def from_list(l):
    temp = l_nil
    for y in reversed(l):
        temp = l_cons(y, temp)
    return temp


def to_list(l):
    return l(lambda x, y: [x] + y, [])


def from_option(o):
    if o is None:
        return o_none
    else:
        return o_some(o)


def to_option(o):
    return o(lambda x: x, None)
