from church_encodings.bool import b_true, b_false, b_and, b_not
from church_encodings.pair import p_pair, p_first, p_second

i_zero = ...
i_succ = ...

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

_phi = ...
i_pred = ...

i_add = ...
i_sub = ...
i_mul = ...

i_is_zero = ...
i_leq = ...
i_lt = ...
i_eq = ...

_div = lambda _div, n, m: i_leq(m, n)(lambda : i_succ(_div(_div, i_sub(n, m), m)), lambda : i_zero)()
i_div = lambda n, m: _div(_div, n, m)

_mod = lambda _mod, n, m: i_leq(m, n)(lambda : _mod(_mod, i_sub(n, m), m), lambda : n)()
i_mod = lambda n, m: _mod(_mod, n, m)

_gcd = lambda _gcd, n, m: i_is_zero(m)(lambda : n, lambda : _gcd(_gcd, m, i_mod(n, m)))()
i_gcd = lambda n, m: _gcd(_gcd, n, m)
