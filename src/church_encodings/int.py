from church_encodings.bool import b_true, b_false, b_and, b_not
from church_encodings.pair import p_pair, p_first, p_second

i_zero = lambda f, x: x
i_succ = lambda n: lambda f, x: f(n(f, x))

i_one   = i_succ(i_zero)
i_two   = i_succ(i_one)
i_three = i_succ(i_two)
i_four  = i_succ(i_three)
i_five  = i_succ(i_four)
i_six   = i_succ(i_five)
i_seven = i_succ(i_six)
i_eight = i_succ(i_seven)
i_nine  = i_succ(i_eight)
i_ten   = i_succ(i_nine)

_phi = lambda p: p_pair(i_succ(p_first(p)), p_first(p))
i_pred = lambda n: p_second(n(_phi, p_pair(i_zero, i_zero)))

i_add = lambda n, m: m(i_succ, n)
i_sub = lambda n, m: m(i_pred, n)
i_mul = lambda n, m: m(lambda k: i_add(n, k), i_zero)

i_is_zero = lambda n: n(lambda _: b_false, b_true)
i_leq = lambda n, m: i_is_zero(i_sub(n, m))
i_lt = lambda n, m: b_not(i_leq(m, n))
i_eq = lambda n, m: b_and(i_leq(n, m), i_leq(m, n))

_div = lambda _div, n, m: i_leq(m, n)(lambda : i_succ(_div(_div, i_sub(n, m), m)), lambda : i_zero)()
i_div = lambda n, m: _div(_div, n, m)

_mod = lambda _mod, n, m: i_leq(m, n)(lambda : _mod(_mod, i_sub(n, m), m), lambda : n)()
i_mod = lambda n, m: _mod(_mod, n, m)

_gcd = lambda _gcd, n, m: i_is_zero(m)(lambda : n, lambda : _gcd(_gcd, m, i_mod(n, m)))()
i_gcd = lambda n, m: _gcd(_gcd, n, m)
