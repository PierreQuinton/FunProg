from .bool import b_true, b_false, b_not, b_or, b_and
from .pair import p_pair, p_first, p_second
from .int import (
    i_zero,
    i_succ,
    i_one,
    i_two,
    i_three,
    i_four,
    i_five,
    i_six,
    i_seven,
    i_eight,
    i_nine,
    i_ten,
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
    i_gcd,
)
from .list import l_nil, l_cons, l_append, l_is_nil, l_is_non_empty, l_head, l_tail, l_filter, l_map, l_flat_map

from .equivalences import from_bool, to_bool, from_int, to_int, from_list, to_list