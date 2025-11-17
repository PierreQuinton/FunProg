# Church Encodings

The goal of this week is to make a fully functional programing paradigm in python.
It is meant as a practical evidence for the [Church-Turing Thesis](https://en.wikipedia.org/wiki/Church%E2%80%93Turing_thesis).
The resulting code is **NOT** efficient, nor is it good practice, but it is a good practical way to introduce functional
thinking.

In order to get a feeling of the power of functional programming, we will define homemade types for
- Booleans
- Pairs (Couples)
- Integers
- Lists

But anything else would in theory be doable. For reference, the theory is available in the file `theory.md`.

## Booleans

We will start by defining booleans. Go to the file `src/church_encodings/bool.py` and start by replacing the `...` by
appropriate lambda expressions. You are expected to implement the lambdas:
- `b_true`
- `b_false`
- `b_not`
- `b_and`
- `b_or`

Next, in order to convince ourselves that our booleans are equivalent to the ones provided by Python, we need to show
that there is a bijection between the two. Go to the file `src/church_encodings/equivalences.py` and fill in the two
functions:
- `from_bool` that takes as an input a Python Boolean and returns a Boolean of our framework.
- `to_bool` that takes as an input one of our Boolean and returns `True` or `False`.

If you want to test if your solutions, you can run pytest on the file `tests/church_encodings/test_bool.py` using your
IDE. You can also test your implementation of equivalence by running pytest on the file
`tests/church_encodings/test_equivalences.py`, only the test `test_bool` should pass.

## Pairs

This is an easy, yet important, part of the lab. Go to the file `src/church_encodings/pair.py` and replace the `...` by
appropriate lambda expressions. You are expected to implement the lambdas:
- `p_pair`
- `p_first`
- `p_second`

Again, in order to convince ourselves that our pairs are equivalent to that of Python, we need to show that there is a 
bijection between the two. Go to the file `src/church_encodings/equivalences.py` and fill in the two functions:
- `from_pair` that takes as an input a Python tuple made of two elements and returns a pair of our framework.
- `to_pair` that takes as an input one of our pair and returns a tuple with two elements.

If you want to test if your solutions, you can run pytest on the file `tests/church_encodings/test_pairs.py` and
`tests/church_encodings/test_equivalences.py` (in which you want `test_pair` to pass) using your IDE.

## Integers

Next, we will define integers and operations on them. Go to the file `src/church_encodings/int.py` and start by
replacing the `...` by appropriate lambda expressions. You are expected to implement the lambdas:
- `i_zero`
- `i_succ`
- `i_pred` and the associated `_phi` function as defined in the theory.
- `i_add`
- `i_sub`
- `i_mul`
- `i_is_zero`
- `i_leq`
- `i_lt`
- `i_eq`
