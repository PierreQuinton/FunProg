from church_encodings.int import i_succ, i_is_zero, i_zero
from church_encodings.option import o_some, o_none, o_map, o_flatmap
from church_encodings.pair import p_pair, p_first, p_second
from church_encodings.bool import b_false, b_true, b_not

l_nil = lambda f, x: x
l_cons = lambda h, t: lambda f, x: f(h, t(f, x))

l_append = lambda l1, l2: l1(l_cons, l2)
l_length = lambda l: l(lambda h, v: i_succ(v), i_zero)
l_is_nil = lambda l: i_is_zero(l_length(l))
l_is_non_empty = lambda l: b_not(l_is_nil(l))

l_filter = lambda l, p: l(lambda h, v: p(h)(l_cons(h, v), v), l_nil)
l_map = lambda l, f: l(lambda h, v: l_cons(f(h), v), l_nil)
l_flatmap = lambda l, f: l(lambda h, v: l_append(f(h), v), l_nil)

l_head = lambda l: l(lambda h, _: o_some(h), o_none)
l_tail = lambda l: p_second(l(lambda h, v: p_pair(l_cons(h, p_first(v)), o_some(p_first(v))), p_pair(l_nil, o_none)))
l_at = lambda l, i: o_flatmap(i(lambda o: o_flatmap(o, l_tail), o_some(l)), l_head)
