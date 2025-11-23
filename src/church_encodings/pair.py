from church_encodings.bool import b_true, b_false

p_pair = lambda x, y: lambda b: b(x, y)

p_first = lambda p: p(b_true)
p_second = lambda p: p(b_false)
