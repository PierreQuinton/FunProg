
b_true = lambda x, y: x
b_false = lambda x, y: y


b_not = lambda b: b(b_false, b_true)
b_and = lambda b1, b2: b1(b2, b_false)
b_or = lambda b1, b2: b1(b_true, b2)
