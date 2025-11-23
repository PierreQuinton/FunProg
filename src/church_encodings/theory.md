## Functional Programming?

This course isn't about becoming a functional programming expert or mastering a specific functional language like Rust.
Instead, our goal is to explore a powerful and elegant way of thinking about and structuring code.

Functional programming isn't just a different style of writing code; it's a new way of approaching problems. You'll
learn to see programming through a different lens, which will give you a powerful new tool for building cleaner, more
reliable, and easier-to-understand programs.

We'll focus on the core ideas that make this programming paradigm so effective, and you'll see how they can be applied
to any language you use, not just specialized functional ones. Ultimately, this course will provide you with a new way
to structure your thoughts and solve problems, which will be valuable no matter what kind of programming you do in the
future.

While functional programming has gained a lot of popularity recently, the ideas behind it are far from new. In fact, its
foundations were laid in the 1930s by mathematician Alonzo Church with the development of lambda calculus.
Interestingly, Church was the doctoral supervisor of Alan Turing, the very person who conceptualized the Turing machine,
the theoretical basis for all modern computers. This means that the two fundamental models of computation, the
imperative model (Turing machines) and the functional model (lambda calculus), have coexisted for nearly a century. The
two models are actually known to be equivalent in their power, a principle known as the Church-Turing thesis.

The functional programing way yields incredibly clean and readable code for even the  most complicated and intricate
software. For example, a portion of the Linux kernel, which runs most of the world's servers, is being rewritten in
Rust, a language that enables the verification of memory safety, thereby preventing common security abuses. Another
example is the Lean software, a fully functional formal verifier that allows mathematicians to write and have their
proofs automatically checked. These are just a few instances that show why functional programming is quickly becoming an
essential skill for software engineers and many other technical professionals.

In essence, functional programming is about describing what something does rather than how it's done. We define things
by their functionality and relationships, not by a step-by-step algorithm. We will immediately put this idea into
practice in our first few labs, where we will attempt to redevelop the base types of Python from scratch by thinking
about their roles. But before we get there, we'll first dive into the theoretical foundation of this approach: an short
introduction to lambda calculus.

While lambda calculus can seem abstract and a bit intimidating at first, the efforts are worthwhile. The goal isn't to
become an expert in lambda calculus, as it can be difficult and impractical on its own. Instead, our purpose is to
practice thinking in the functional way.

## Functions as values

Lambda calculus begins with the concept of $\lambda$ expression, a notation for defining a function. This may be
familiar to some of you who have encountered Python's `lambda` keyword, which is used to create an inline function.

For example:
```python
f = lambda x: x ** 2   # A function mapping some x to its square
f(4)                   # 16
f(-7)                  # 49
```

Similarly, in lambda calculus, the expression
<!--math-->
$$
\lambda\hspace{0.4em}x, x^2
$$
<!--endmath-->
represents the function mapping some $x$ to its square $x^2$.

In lambda calculus, applying a function $f$ to a value $x$ is written as $f\hspace{0.4em}x$, omitting the parentheses typically used
in other notations like $f(x)$. The primary reason for this is to avoid overly nested parentheses: you don't want to
write $f(g(h(f(d(x)))))$. Parentheses are still used to specify the order of operations. For example $f\hspace{0.4em}(g\hspace{0.4em}x)$
represents applying $f$ to the result of applying $g$ to $x$. It's important to note that this is different from
$g\hspace{0.4em}f\hspace{0.4em}x$, which is the same as $(g\hspace{0.4em}f)\hspace{0.4em}x$.

Since $\lambda\hspace{0.4em}x, x^2$ is a function, we can apply it to a value. For instance
<!--math-->
$$
(\lambda\hspace{0.4em}x, x^2)\hspace{0.4em}2
$$
<!--endmath-->
evaluates to $4$.
In python this can be directly translated to
```python
(lambda x: x ** 2)(2)  # 4
```

What if we want to apply the same function to several inputs without redefining it every time? We can assign it a
name by defining a lambda expression that binds the function to a variable. For example, consider the expression:
<!--math-->
$$
\big(\lambda\hspace{0.4em}f, f\hspace{0.4em}(f\hspace{0.4em}3)\big)(\lambda\hspace{0.4em}x, x^2)
$$
<!--endmath-->
evaluates to $81$. This works because we are applying the function $(\lambda\hspace{0.4em}f,f\hspace{0.4em}(f\hspace{0.4em}3))$ to the value $(\lambda\hspace{0.4em}x, x^2)$
(which is a function). So, $f$ becomes $\lambda\hspace{0.4em}x,x^2$. We then evaluate $f\hspace{0.4em}3$, which is $3^2=9$, and then apply $f$ to
that result, giving us $f\hspace{0.4em}9$, which is $9^2=81$.

In Python, if we didn't have the `def` keyword, we could achieve a similar result by nesting lambdas:
```python
(lambda f: f(f(3)))(lambda x: x ** 2)  # 81
```
This is a slightly uglier but equivalent way of writing
```python
def f(x):
    return x ** 2

f(f(3))
```
But there is nothing that the `def` keyword can do that can't be done with the `lambda` keyword.

This brings us to what is arguably the most important concept in all of functional programming: functions are values.
This powerful idea means that functions are treated just like any other value, such as a number or a string. They can be
passed as arguments to other functions, and returned as the result of a function. Understanding this single principle
will be key to truly unlock the functional mindset.

Let's experiment with this idea by defining a function that takes another function as input and returns its composition
with itself. In lambda calculus, we can write this as:
<!--math-->
$$
\lambda\hspace{0.4em}f, \lambda\hspace{0.4em}x, f\hspace{0.4em}(f\hspace{0.4em}x)
$$
<!--endmath-->
This expression defines a function that, when given an input function $f$, returns the function $\lambda\hspace{0.4em}x, f\hspace{0.4em}(f\hspace{0.4em}x)$.
This function, takes an argument $x$ and applies $f$ to it twice. Overall, when we apply this function to some $f$, it
returns the composition $f \circ f$ of $f$ with itself. 

We can use this to compute the fourth power of a number from the square function. Consider the following expression,
where we apply our composition function to the squaring function $(\lambda\hspace{0.4em}x, x^2)$ and the number $2$:
<!--math-->
$$
\big(\lambda\hspace{0.4em}f, \lambda\hspace{0.4em}x, f\hspace{0.4em}(f\hspace{0.4em}x)\big)\hspace{0.4em}(\lambda\hspace{0.4em}x, x^2)\hspace{0.4em}2
$$
<!--endmath-->
Evaluating this will yield the following steps (we change the name of some variable $x$ to make it more readable)
$$\begin{align*}
& \big(\lambda\hspace{0.4em}f, \lambda\hspace{0.4em}x, f\hspace{0.4em}(f\hspace{0.4em}x)\big)\hspace{0.4em}(\lambda\hspace{0.4em}x, x^2)\hspace{0.4em}2\\
\to\hspace{0.4em}& \bigg(\lambda\hspace{0.4em}x, \Big((\lambda\hspace{0.4em}y, y^2)\hspace{0.4em}\big((\lambda\hspace{0.4em}z, z^2)\hspace{0.4em}x\big)\Big)\bigg)\hspace{0.4em}2&&
\big(\text{replace $f$ with $(\lambda\hspace{0.4em}x, x^2)$}\big)\\
\to\hspace{0.4em}& (\lambda\hspace{0.4em}y, y^2)\hspace{0.4em}\big((\lambda\hspace{0.4em}z, z^2)\hspace{0.4em}2\big)&&
\big(\text{replace $x$ with $2$}\big)\\
\to\hspace{0.4em}& (\lambda\hspace{0.4em}y, y^2)\hspace{0.4em}4&&
\big(\text{replace $z$ with $2$}\big)\\
\to\hspace{0.4em}& 16&&
\big(\text{replace $y$ with $4$}\big)\\
\end{align*}<!--math-->
$$

In Python, this translates to a very similar structure
```python
(lambda f: lambda x: f(f(x)))(lambda x: x**2)(-2)  # 16
```

This example shows how we can effectively bind a value for later use. In Python, we would typically do this with an
assignment statement like this:
```python
f = ...
x = ...
f(x)
```
In raw lambda calculus, this can be accomplished with a somewhat impractical nested expression:
<!--math-->
$$
(\lambda\hspace{0.4em}f, \lambda\hspace{0.4em}x, f\hspace{0.4em}x)\hspace{0.4em}(\dots)\hspace{0.4em}(\dots)
$$
<!--endmath-->
Because writing this out every time would be tedious, we introduce some syntactic sugar to make it easier to read and
write. This means we're creating convenient shortcuts that translate directly into lambda calculus.

For instance, the following common notation:
<!--math-->
$$
\begin{align*}
x ={}& \text{expr}_1\\
&\text{expr}_2
\end{align*}
$$
<!--endmath-->
is simply another way of writing:
<!--math-->
$$
(\lambda\hspace{0.4em}x, \text{expr}_2)\hspace{0.4em}(\text{expr}_1)
$$
<!--endmath-->
Another piece of syntactic sugar we will use is to combine multiple $\lambda$ abstractions. So, instead of writing:

<!--math-->
$$
\lambda\hspace{0.4em}x, \lambda\hspace{0.4em}y, \lambda\hspace{0.4em}z, \text{expr}
$$
<!--endmath-->
we can write the more compact form:
<!--math-->
$$
\lambda\hspace{0.4em}x\hspace{0.4em}y\hspace{0.4em}z, \text{expr}
$$
<!--endmath-->

With these simplified notations, we are now ready to define more interesting and complex constructs.

## Values as functions

Now that we have the basic tools, let's explore what we can actually build with lambda calculus. The rather surprising
answer is anything a computer (or, more formally, a Turing machine) can do.

In the previous section, we cheated a little by assuming that numbers and other basic types existed. But in pure lambda
calculus, we can't assume anything. We have to build everything from scratch. So, let's begin by defining some of the
builtins types you're familiar with in Python.

This brings us to the second main takeaway from this course: in functional programming, types are defined by their
roles. To illustrate this principle, let's start with Booleans.

### Boolean

The primary purpose of a Boolean is to act as a switch, typically seen in `if`/`else` statements such as
the following:
```python
if b:
    z = x
else:
    z = y
```
This code snippet shows that a Boolean's role is to select between one of two values or actions. For this reason, we can
represent a Boolean as a function that chooses between its two arguments.

We define $\mathrm{true}$ and $\mathrm{false}$ as follows:
<!--math-->
$$\begin{align*}
\mathrm{true} &= \lambda\hspace{0.4em}x\hspace{0.4em}y, x\\
\mathrm{false} &= \lambda\hspace{0.4em}x\hspace{0.4em}y, y
\end{align*}$$
<!--endmath-->
With these definitions, $\mathrm{true}$ is a function that always returns the first value it's given, while $\mathrm{false}$ always
returns the second. This allows the Python code to be translated into the elegant and simple lambda calculus expression:
<!--math-->
$$
z = b\hspace{0.4em}x\hspace{0.4em}y
$$
<!--endmath-->

Of course, Booleans are only useful if we can combine them with logical operations like `or`, `and` and `not`.
We can easily implement $\mathrm{not}$ as
<!--math-->
$$
\mathrm{not} = \lambda\hspace{0.4em}b, b\hspace{0.4em}\mathrm{false}\hspace{0.4em}\mathrm{true}
$$
<!--endmath-->
If $b$ is $\mathrm{true}$, this evaluates to $\mathrm{false}$, and if $b$ is $\mathrm{false}$, it evaluates to $\mathrm{true}$, just as we would
expect.

Take a moment to reflect on the simplicity and elegance of this idea. All of this power and grace comes from one
fundamental concept: treating functions as first-class values.

Let's now move on to the $\mathrm{or}$ operator. It takes two Booleans $b_1$ and $b_2$, and returns $\mathrm{true}$ if either one is
$\mathrm{true}$, and $\mathrm{false}$ otherwise. We can rephrase this logic in a way that's perfect for a functional definition: If
$b_1$ is $\mathrm{true}$, return $\mathrm{true}$, otherwise return $b_2$.

Since our Booleans act as selectors, where $\mathrm{true}$ selects the first argument and $\mathrm{false}$ selects the second, we can
implement this logic by calling $b_1$ with the appropriate arguments. 
This yields the following elegant definition for $\mathrm{or}$:
<!--math-->
$$
\mathrm{or} = \lambda\hspace{0.4em}b_1\hspace{0.4em}b_2, b_1\hspace{0.4em}\mathrm{true}\hspace{0.4em}b_2
$$
<!--endmath-->
Take a moment to truly understand this definition. To fully grasp the logic, try evaluating this expression by
substituting $\mathrm{true}$ and $\mathrm{false}$ for $b_1$ and $b_2$ in all four possible combinations. This exercise will help you
see how the simple act of function application performs the exact logical operation you expect.

Let's define the final logical operator, $\mathrm{and}$. This operator takes two Booleans, $b_1$ and $b_2$, and returns
$\mathrm{true}$ only if both are $\mathrm{true}$, and $\mathrm{false}$ otherwise. We can rephrase this logic using our functional approach:
If $b_1$ is $\mathrm{true}$, the result should be $b_2$. Otherwise, the result should be $\mathrm{false}$.

This leads to the following elegant definition for $\mathrm{and}$:
<!--math-->
$$
\mathrm{and} = \lambda\hspace{0.4em}b_2\hspace{0.4em}b_2, b_1\hspace{0.4em}b_2\hspace{0.4em}\mathrm{false}
$$
<!--endmath-->
Notice how this definition perfectly mirrors the logic. If $b_1$ is $\mathrm{true}$, it will select its first argument, which
is $b_2$. If $b_1$ is $\mathrm{false}$, it will select its second argument, which is $\mathrm{false}$, giving us the correct result in
both cases. Take a moment to trace the evaluation with different combinations of inputs for $b_1$ and $b_2$ to see this
in action.

### Pair
Next, we'll define a pair of values. This is a foundational step, as more complex data structures like tuples can be
bumathrm{lt} by nesting pairs (a tuple of three elements is just a pair of a value and another pair).

A pair's core role is to contain two values and provide a way to access each of them. With this role in mind, we can
view a pair as a function that maps an index to a value. And what better index to use than our newly defined Booleans?
We can define a pair as a function that maps $\mathrm{true}$ to the first value and $\mathrm{false}$ to the second.

With this, we can now define a suitable constructor for pairs, a function we'll call $\mathrm{pair}$. It takes two values and
returns a function that acts as their pair.

Formally:
<!--math-->
$$
\mathrm{pair} = \lambda\hspace{0.4em}x\hspace{0.4em}y, \lambda\hspace{0.4em}b, b\hspace{0.4em}x\hspace{0.4em}y.
$$
<!--endmath-->

We can also define getters to retrieve the values from a pair, functions that map a pair to either its first or second
element:
<!--math-->
$$\begin{align*}
\mathrm{first} &= \lambda\hspace{0.4em}p, \mathrm{true}\hspace{0.4em}p\\
\mathrm{second} &= \lambda\hspace{0.4em}p, \mathrm{false}\hspace{0.4em}p
\end{align*}$$
<!--endmath-->
Notice that since our pair is a function that takes a Boolean as input, all we have to do is apply the pair to $\mathrm{true}$
or $\mathrm{false}$ to retrieve the corresponding element.

As an exercise, you should verify that $\mathrm{first}\hspace{0.4em}(\mathrm{pair}\hspace{0.4em}x\hspace{0.4em}y)$ evaluates to $x$ while $\mathrm{second}\hspace{0.4em}(\mathrm{pair}\hspace{0.4em}x\hspace{0.4em}y)$ evaluates
to $u$.

### Integer
The most common use of an integer is to perform an action a certain number of times, as seen in a `for` loop. For
example, in the following Python code, the number `n` dictates how many times we add `1` to `sum`:


The typical usage of an integer is in a for loop over some range. For example in the following Python code:
```python
sum = 0
for _ in range(n):
    sum += 1
```
In other words, The core role of an integer is simply to act as a counter that tells us how many times to repeat an
operation.

Based on this role, we can define integers in lambda calculus as operators that apply a function a number of times
corresponding to the value they represent. If $f$ is the function being applied and $x$ is the initial value, then:
- $0$ maps $f$ and $x$ to $x$ (it applies the function zero times).
- $1$ maps $f$ and $x$ to $f(x)$ (one application).
- $2$ maps $f$ and $x$ to $f\big(f(x)\big)$ (two applications).
- $3$ maps $f$ and $x$ to $f\Big(f\big(f(x)\big)\Big)$ (three applications).

In the Python example above, you can think of the initial value $x=0$ and the function $f : y\mapsto y+1$.

Note that to define any integer, we only need to define $0$ and a way to get the successor of any integer (i.e., the
next integer). For instance, the number $2$ is the successor of the successor of $0$.

This leads to the following elegant definitions in lambda calculus, often called Church numerals:
<!--math-->
$$\begin{align*}
\mathrm{zero} &= \lambda\hspace{0.4em}f\hspace{0.4em}x, x\\
\mathrm{succ} &= \lambda\hspace{0.4em}n, \lambda\hspace{0.4em}f\hspace{0.4em}x, f\hspace{0.4em}(n\hspace{0.4em}f\hspace{0.4em}x)
\end{align*}$$
<!--endmath-->

As an exercise, verify that if $\text{two}=\mathrm{succ}\hspace{0.4em}(\mathrm{succ}\hspace{0.4em}\mathrm{zero})$, it represents a function that maps $f$ and $x$ to
$f\big(f(x)\big)$, and convince yourself that this logic should extend to any integer.

Now that we have our building blocks, let's see how we can perform operations on them. Let's start with a simple one:
adding two numbers.

We can define addition by thinking about what it really means. For example, to get $5$ from $2+3$, we can apply the
successor function three times, starting from $2$. In our lambda calculus world, three is a function that applies
another function $f$ three times to some initial value $x$. So, if we choose $f$ to be the successor function $\mathrm{succ}$
and $x$ to be the number two, we get:
<!--math-->
$$
\text{five} = \text{three}\hspace{0.4em}\mathrm{succ}\hspace{0.4em}\text{two}
$$
<!--endmath-->
Generalizing this, we can define addition as a function that takes two numbers, $n$ and $m$, and applies the successor
function $m$ times to $n$. This leads to the following elegant definition:
<!--math-->
$$
\mathrm{add} = \lambda\hspace{0.4em}n\hspace{0.4em}m, m\hspace{0.4em}\mathrm{succ}\hspace{0.4em}n.
$$
<!--endmath-->
Take a moment to convince yourself why this is correct. If you apply $\mathrm{add}$ to two and three, the number three will
take $\mathrm{succ}$ and two as its arguments, applying $\mathrm{succ}$ three times to two, which correctly gives us five.

The integers we've defined are non-negative. While it's possible to extend these concepts to include negative numbers,
we won't go into that here. However, we can still define subtraction, as long as the result is not negative.

Just as we used $\mathrm{succ}$ to define the operation of adding one, we can define a predecessor function, $\mathrm{pred}$, that
decreases a number by one. This will be valid for any number greater than or equal to one. For practicality, we'll
define $0-1$ to be equal to $0$.

It might not be immediately obvious how to create this $\mathrm{pred}$ function using only our successor function. One way to
approach it is to think about it with a for loop that keeps track of both the current value and the preceding one. In
Python, this would look something like this:
```python
def pred(n: int):
    preceding = 0
    current = 0
    for _ in range(n):
        preceding = current
        current = current + 1
    return preceding
```
If you provide `1` as an argument to pred, it returns `0`. If you provide `n > 1`, it correctly returns `n-1` (and note
that current will always be equal to `n`).

We can replicate this logic in lambda calculus using our pairs and the ability to apply functions iteratively. Our goal
is to define a function that:
- Takes a pair `(current, preceding)` as an argument.
- Returns a new pair, where the new `current` value is the successor of the old `current` value, and the new `preceding`
  value is the old `current` value.
- Starts with an initial pair of `(0, 0)`.
- After iterating, takes the second element of the final pair (which corresponds to the `preceding` value we want).

This leads to the following formal definition for $\mathrm{pred}$:
<!--math-->
$$\begin{align*}
\phi &= \lambda\hspace{0.4em}p, \mathrm{pair}\hspace{0.4em}\big(\mathrm{succ}\hspace{0.4em}(\mathrm{first}\hspace{0.4em}p)\big)\hspace{0.4em}(\mathrm{first}\hspace{0.4em}p)\\
\mathrm{pred} &= \lambda\hspace{0.4em}n, \mathrm{second}\hspace{0.4em}\big(n\hspace{0.4em}\phi\hspace{0.4em}(\mathrm{pair}\hspace{0.4em}\mathrm{zero}\hspace{0.4em}\mathrm{zero})\big)
\end{align*}$$
<!--endmath-->
Take a moment to carefully trace the logic here. The variable $n$ is used to apply $\phi$ a total of $n$ times to the
initial pair $(\mathrm{zero}, \mathrm{zero})$. After all the applications, $\mathrm{second}$ retrieves the final preceding value, giving us
our desired result.

Now that we have defined $\mathrm{pred}$, it becomes very easy to define substraction. Recall that addition was implemented by
apply the successor function an appropriate number of times to a provided number. Similarly, subtraction can be defined
by apply the predecessor function several time to a number. Specifically
<!--math-->
$$
\mathrm{sub} = \lambda\hspace{0.4em}n\hspace{0.4em}m, m\hspace{0.4em}\mathrm{pred}\hspace{0.4em}n.
$$
<!--endmath-->
Make sure you understand that applying $m$ times $\mathrm{pred}$ to $n$ indeed yields $m-n$. Also note that if $n$ is larger
than $m$, we get $0$.

Multiplication is also quite simple. When computing $n\times m$, we are basically adding $n$ to $0$, $m$ times:
<!--math-->
$$\begin{align*}
n\times m = n+\dots+n+0
\end{align*}$$
<!--endmath-->
In lambda calculus, this translates directly to
<!--math-->
$$
\mathrm{mul} = \lambda\hspace{0.4em}n\hspace{0.4em}m, m\hspace{0.4em}(\lambda\hspace{0.4em}k, \mathrm{add}\hspace{0.4em}n\hspace{0.4em}k)\hspace{0.4em}\mathrm{zero}.
$$
<!--endmath-->
Make sure you understand this expression. Note that $\lambda\hspace{0.4em}k, \mathrm{add}\hspace{0.4em}n\hspace{0.4em}k$ is a function that takes an integer $k$ and
outputs $k+n$, i.e., it is the "add $n$" function. If we apply this function $m$ times to $0$, we are adding $m\times n$
to $0$, which is indeed $m\times n$.

Now it becomes truely interesting. We will implement some relations on the integers such as `<=` or `==`. These
operations take as input two integers and output a Boolean. But we have defined Booleans so we can make them output one
of our homemade Booleans.

Let us start slow by implementing a function that tests if an integer is $\mathrm{zero}$. As our numbers are defined by the
number of times they apply a function to an initial value, we want our function to yield $\mathrm{true}$ if and only if the
function is applied $0$ times, and $\mathrm{false}$ otherwise. So the function we apply should always return $\mathrm{false}$ and the
initial value should be $\mathrm{true}$. In Python this code would look something like this:
```python
def is_zero(n):
    result = True
    for _ in range(n):
        result = False
    return result
```
And this indeed returns `True` if and only if `n == 0`. In lambda calculus, we can write this as
<!--math-->
$$
\mathrm{isZero}=\lambda\hspace{0.4em}n,n\hspace{0.4em}(\lambda\hspace{0.4em}x,\mathrm{false})\hspace{0.4em}\mathrm{true}.
$$
<!--endmath-->
Make sure to verify that this is indeed a translation of the above python code in lambda calculus.

This operator will enable us to define comparison operators such as $\leq$, $<$ and $=$. Recall that when we computed
$\mathrm{sub}\hspace{0.4em}n\hspace{0.4em}m$, we would get $\mathrm{zero}$ whenever $n\leq m$. So by combining $\mathrm{sub}$ and $\mathrm{isZero}$, we can implement the
operator $\leq$ to compare elements:
<!--math-->
$$
\mathrm{leg}=\lambda\hspace{0.4em}n\hspace{0.4em}m, \mathrm{isZero}\hspace{0.4em}(\mathrm{sub}\hspace{0.4em}n\hspace{0.4em}m).
$$
<!--endmath-->
Also note that in python `n < m` is always equal to `not (m <= n)`, so we can implement the `<` operator as
<!--math-->
$$
\mathrm{lt}=\lambda\hspace{0.4em}n\hspace{0.4em}m, \mathrm{not}\hspace{0.4em}(\mathrm{leg}\hspace{0.4em}m\hspace{0.4em}n).
$$
<!--endmath-->
Last but not least, we also have `n == m` if and only if both `n <= m` and `m <= n` hold, so we can implement the `==`
operator as
<!--math-->
$$
\mathrm{eq}=\lambda\hspace{0.4em}n\hspace{0.4em}m, \mathrm{and}\hspace{0.4em}(\mathrm{leg}\hspace{0.4em}n\hspace{0.4em}m)\hspace{0.4em}(\mathrm{leg}\hspace{0.4em}m\hspace{0.4em}n).
$$
<!--endmath-->
Make sure you understand why these three operators work and verify that they are correct.
