from church_encodings.bool import b_true, b_false

o_none = lambda f, y: y
o_some = lambda x: lambda f, y: f(x)

o_is_none = lambda o: o(lambda x: b_false, b_true)
o_is_some = lambda o: o(lambda x: b_true, b_false)
o_get_or_else = lambda o, y: o(lambda x: x, y)

o_map = lambda o, f: o(lambda x: o_some(f(x)), o_none)
o_flatmap = lambda o, f: o(lambda x: f(x), o_none)
