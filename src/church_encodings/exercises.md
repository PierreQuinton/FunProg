# Church Encodings

The goal of this week is to make a fully functional programing paradigm in python.
It is meant as a practical evidence for the [Church-Turing Thesis](https://en.wikipedia.org/wiki/Church%E2%80%93Turing_thesis).
The resulting code is **NOT** efficient, nor is it good practice, but it is a good practical way to introduce functional
thinking.

In order to get a feeling of the power of functional programming, we will define homemade types for
- Booleans
- Pairs (Couples)
- Integers
- Options
- Lists

But anything else would in theory be doable. For reference, the theory is available in the file `theory.md`.

## Testing your code

At any point, you can check your progress by running, from the root of the repository:

```
python run_tests.py
```

This does not require anything to be installed besides Python. For each group of exercises, it tells you whether the tests pass (`OK`), whether some of them fail because your result is wrong (`FAIL`), or whether they hit something you have not implemented yet (`TODO`). Add the flag `-v` to see one line per test.

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

If you want to test your solutions, you can run `python run_tests.py`. You want the line `bool` to be `OK`. You can also
look at the line `equivalences`, in which only the test `test_bool` should pass at this point.

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

If you want to test your solutions, you can run `python run_tests.py`. You want the line `pair` to be `OK`, as well as
the test `test_pair` of the line `equivalences`.

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

The constants from `i_one` to `i_ten` are already provided, they are defined in terms of `i_zero` and `i_succ`, so you
should start by implementing those two.

Again, in order to convince ourselves that our integers are equivalent to the ones provided by Python, we need to show
that there is a bijection between the two. Go to the file `src/church_encodings/equivalences.py` and fill in the two
functions:
- `from_int` that takes as an input a Python integer and returns an Integer of our framework.
- `to_int` that takes as an input one of our Integer and returns the corresponding Python integer.

If you want to test your solutions, you can run `python run_tests.py`. You want the line `int` to be `OK`, as well as
the test `test_int` of the line `equivalences`.

## Options

We will now define options. An option is a container that is either empty or contains exactly one value, this is our way
of handling the absence of a value, where Python would use `None`. Go to the file `src/church_encodings/option.py` and
replace the `...` by appropriate lambda expressions. You are expected to implement the lambdas:
- `o_none`
- `o_some`
- `o_is_none`
- `o_is_some`
- `o_get_or_else`
- `o_map`
- `o_flatmap`

Again, in order to convince ourselves that our options are equivalent to what Python does with `None`, we need to show
that there is a bijection between the two. Go to the file `src/church_encodings/equivalences.py` and fill in the two
functions:
- `from_option` that takes as an input a Python value that may be `None` and returns an Option of our framework.
- `to_option` that takes as an input one of our Option and returns the value it contains, or `None` if it is empty.

If you want to test your solutions, you can run `python run_tests.py`. You want the line `option` to be `OK`.

## Lists

Finally, we will define lists, the most versatile structure of this lab. Go to the file `src/church_encodings/list.py`
and replace the `...` by appropriate lambda expressions. You are expected to implement the lambdas:
- `l_nil`
- `l_cons`
- `l_append`
- `l_length`
- `l_is_nil`
- `l_is_non_empty`
- `l_filter`
- `l_map`
- `l_flatmap`
- `l_head`
- `l_tail`
- `l_at`

The last three functions output options since the requested element may not exist. Note that `l_tail` and `l_at` are
the hardest functions of this lab, you will probably need to read the theory of lists before implementing them.

Again, in order to convince ourselves that our lists are equivalent to the ones provided by Python, we need to show
that there is a bijection between the two. Go to the file `src/church_encodings/equivalences.py` and fill in the two
functions:
- `from_list` that takes as an input a Python list and returns a List of our framework.
- `to_list` that takes as an input one of our List and returns the corresponding Python list.

If you want to test your solutions, you can run `python run_tests.py`. You want the line `lists` to be `OK`, as well as
the test `test_list` of the line `equivalences`.
