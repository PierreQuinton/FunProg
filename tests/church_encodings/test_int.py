from pytest import mark

from church_encodings.int import (
    i_zero,
    i_succ,
    i_pred,
    i_add,
    i_mul,
    i_sub,
    i_is_zero,
    i_leq,
    i_lt,
    i_eq,
    i_div,
    i_mod,
)
from church_encodings.equivalences import from_bool, from_int, to_int

f = lambda x: x + 1
x = 0

def test_zero():
    assert to_int(i_zero) == 0


@mark.parametrize("n", [2, 5, 6])
def test_succ(n):
    i_n = from_int(n)
    assert to_int(i_succ(i_n)) == n + 1


@mark.parametrize("n", [3, 6, 7])
def test_pred(n):
    i_n = from_int(n)
    assert to_int(i_pred(i_n)) == n - 1


def test_pred_zero_is_zero():
    assert i_pred(i_zero) == i_zero


@mark.parametrize("n", [0, 1, 2])
def test_is_zero(n):
    i_n = from_int(n)
    assert i_is_zero(i_n) == from_bool(n == 0)


@mark.parametrize("n", [0, 3, 5, 6, 8])
@mark.parametrize("m", [0, 1, 5, 11])
def test_leq(n, m):
    i_n = from_int(n)
    i_m = from_int(m)
    assert i_leq(i_n, i_m) == from_bool(n <= m)


@mark.parametrize("n", [0, 3, 5, 6, 8])
@mark.parametrize("m", [0, 1, 5, 11])
def test_lt(n, m):
    i_n = from_int(n)
    i_m = from_int(m)
    assert i_lt(i_n, i_m) == from_bool(n < m)


@mark.parametrize("n", [0, 3, 5, 6, 8])
@mark.parametrize("m", [0, 1, 5, 11])
def test_eq(n, m):
    i_n = from_int(n)
    i_m = from_int(m)
    assert i_eq(i_n, i_m) == from_bool(n == m)


@mark.parametrize("n", [0, 3, 5, 6, 8])
@mark.parametrize("m", [0, 1, 5, 11])
def test_add(n, m):
    i_n = from_int(n)
    i_m = from_int(m)
    assert to_int(i_add(i_n, i_m)) == n + m


@mark.parametrize("n", [0, 3, 5, 6, 8])
@mark.parametrize("m", [0, 1, 5, 11])
def test_mul(n, m):
    i_n = from_int(n)
    i_m = from_int(m)
    assert to_int(i_mul(i_n, i_m)) == n * m


@mark.parametrize("n", [0, 3, 5, 6, 8])
@mark.parametrize("m", [0, 1, 5, 11])
def test_sub(n, m):
    if n < m:
        return
    i_n = from_int(n)
    i_m = from_int(m)
    assert to_int(i_sub(i_n, i_m)) == n - m


@mark.parametrize("n", [0, 3, 5, 6, 8])
@mark.parametrize("m", [1, 5, 11])
def test_div(n, m):
    i_n = from_int(n)
    i_m = from_int(m)
    assert to_int(i_div(i_n, i_m)) == n // m


@mark.parametrize("n", [0, 3, 5, 6, 8])
@mark.parametrize("m", [1, 5, 11])
def test_mod(n, m):
    i_n = from_int(n)
    i_m = from_int(m)
    assert to_int(i_mod(i_n, i_m)) == n % m


@mark.parametrize("n", [0, 3, 5, 6, 8])
@mark.parametrize("m", [0, 1, 5, 11])
def test_gcd(n, m):
    if n == 0 and m == 0:
        return
    if n <= m:
        k = m
    else:
        k = n
    gcd = 1
    for i in range(1, k+1):
        if n % k == 0 and m % k == 0:
            gcd = k
    i_n = from_int(n)
    i_m = from_int(m)
    assert to_int(i_gcd(i_n, i_m)) == gcd
