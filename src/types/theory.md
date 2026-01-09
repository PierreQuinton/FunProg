# The Architecture of Roles: An Introduction to Typing

In the previous module on Lambda Calculus, we established that the most important aspect of an object is its role: what it does within a system. As we transition toward Object-Oriented Programming and complex systems, we need a formal way to organize these roles. This is the essence of **typing**.

A **type** is more than just a label; it is a way to structure levels of abstraction. By assigning a type to an object, you are defining how it is intendeed to interact.

The **type checker** acts as a logic verifier. Its role is to ensure that the interactions between your objects are sound. If a program is well-typed, it means the logic of your abstractions is coherent. If a program doesn't pass type checking, then the structure is most likely not logically sound.

The objective of this course is to introduce typing through an order theoretical view. We will overview mathematical notions of order theory such as partial orders, lattices, and we will see how typing is inscribed into this perspective.

### The Subtyping Relation: $\preceq$

The most fundamental relation in typing is **subtyping**. We typically say that a type $S$ is a subtype of $T$ if we can naturally say that "$S$ is a $T$". For instance "a `Human` is an `Animal`". This is rather vague, and to make this mathematically precise, we use the Liskov substitution principle:

> We say that $S$ is a subtype of $T$, denoted as $S\preceq T$, if and only if:
>
> An object of type $S$ may be substituted for an object of type $T$ without altering any of the desirable properties of the program.

In other words, if your code expects a $T$, it should be able to receive an $S$ and continue to function perfectly.

A relation $\leq$ is a **partial order** if it satisfies the three properties:
1. Reflexivity: $a\leq a$.
2. Antisymmetry: If $a\leq b$ and $b\leq a$, then $a=b$.
3. Transitivity: If $a\leq b$ and $b\leq c$, then $a\leq c$.

> **Exercises:**
> 1. Prove that subtyping, as defined by the Liskov substitution principle, is a partial order.
> 2. Try to list other orders that you know of and prove that they are partial orders.


### The Variance of Functions

When we want to consider functions as types, we encounter the notion of dependent types (types that depend on other types, like `list[int]` in Python).

Suppose we have a function type defined by its input of type $T$ and its output of type $S$, we denote the type of this function as $T\to S$. In Python, this would be a `Callable[[T], S]`.

To avoid long phrases, we will adopt the notation $x:T$ to mean "$x$ is an object of type $T$". In particular, $f:T\to S$ reads as "$f$ is a function that takes some object of type $T$ as input and outputs an object of type $S$".

> **Exercise:** Prove that $(T_1\to S_1) \preceq (T_2\to S_2) \hspace{0.4em}\Leftrightarrow \hspace{0.4em} (T_2\preceq T_1) \land (S_1\preceq S_2)$

In other words, if we have a function $f_2:T_2\to S_2$, we can safely substitute it with a function $f_1:T_1\to S_1$ if:
1. $S_1\preceq S_2$. The new function returns something more specific (or the same) than requested.
2. $T_2\preceq T_1$. The new function must be able to handle at least everything the original could, meaning its input requirement is broader.

As an illustration, convince yourself that a function that outputs a `Dog` is a function that outputs an `Animal`. Conversely, if we have a function that accepts any `Animal` as an input, then surely it accepts any `Dog` as an input.

This provides us with natural definition of Covariance and Contravariance of dependent types. Consider the dependent type $T[S]$ ($T$ depends on $S$), then:
1. $T$ is covariant if $S_1\preceq S_2$ implies $T[S_1]\preceq T[S_2]$. In order theory, we call this a monotonic function.
2. $T$ is contravariant if $S_1\preceq S_2$ implies $T[S_2] \preceq T[S_2]$. In order theory, we call this an antimonotonic function.

So the function type is contravariant in its input type, and covariant in its output type.

> **Exercise:** Determine if the dependent type $L[T]$ of lists of elements of type $T$ is covariant or contravariant in $T$.

### Type Systems as Lattices

If we view types through the lens of order theory, the subtyping relation $\preceq$ organizes types into a complete lattice. A lattice is a partial order where every pair of elements have a least upper bound (called supremum) and a greatest lower bound (called infimum):
1. Supremum: $a\lor b$ is the supremum of $a$ and $b$ if $a\leq a\lor b$ and $b\leq a\lor b$, and any $c$ with $a\leq c$ and $b\leq c$ satisfies $a\lor b\leq c$. In plain english $a\lor b$ is an upper bound of $a$ and $b$, and is smaller than any other upper bound.
2. Infimum: $a\land b$ is the infimum of $a$ and $b$ if $a\land b\leq a$ and $a\land b$, and any $c$ with $c\leq a$ and $c\leq b$ satisfies $c\leq a\land b$. In plain english $a\land b$ is a lower bound of $a$ and $b$, and is larger than any other lower bound.

> **Exercises:** Show that
> 1. The supremum of two types $T$ and $S$ is the union type $S\cup T$. An object of that type is either an object of type $S$ or an object of type $T$.
> 2. The infimum of two types $T$ and $S$ is the intersection type $S\cap T$. An object of that type is of type $S$ and of type $T$ at the same time, it is also the largest type such that this is true.
> 3. Are $S\cup T$ and $S\cap T$ covariant/contravariant in $S$ and in $T$?
> 4. Prove that the operations of infimum and supremum are associative: for any $a, b, c$, $a\lor(b\lor c)=(a\lor b)\lor c$ and $a\land (b\land c)=(a\land b)\land c$.

Associativity is very important, it means that the least upper bound and greatest lower bound of three elements $a, b, c$ are unambiguous.
More generally, in a lattice, we can take the supremum and infimum of a finite collection of elements.
This itself isn't enough to say that the infimum and supremum of arbitrary (infinite) collections of types have a supremum and an infimum. Note that we do already have a way of building infinitely many types, as long as we have at least one type $T$ available, this is because we can have $T$, $T\to T$, $T\to T \to T$, ...

> **Exercises:** Prove that 
> 1. If we have an arbitrary collection $C$ of types, then the least upper bound of $C$ is $\bigcup_{T\in C} T$: an element of that type satisfies the existence of some $T$ in $C$ such that the element is of type $T$.
> 2. If we have an arbitrary collection $C$ of types, then the greatest lower bound of $C$ is $\bigcap_{T\in C} T$: an element of that type is of type $T$ for all $T\in C$, furthermore, it is the largest type such that this is true.

A lattice whose every subset has a supremum and an infiumum is called a complete lattice. Actually we only need one of the two: If a lattice satisfies that any subset has a supremum, then for any set $C$, we can take the supremum of the lower bounds of $C$, this is an infimum of $C$. The converse is also true.

We showed that the lattice of types is complete. If we take the supremum of all types, we get the maximal type with respect to the subtyping relation $\preceq$. We call this element the top type, and we denote it by $\top$.
Similarly, we can take the infimum of all types, we get the bottom type $\bot$.

> **Exercices:** Show that:
> 1. If $T[S]$ is a covariant dependent type and $C$ a collection of types, then $\bigcup_{S\in C} T[S]=T\left[\bigcup_{S\in C} S\right]$ and $\bigcap_{S\in C} T[S]=T\left[\bigcap_{S\in C} S\right]$.
> 2. If $T[S]$ is a contravariant dependent type and $C$ a collection of types, then $\bigcup_{S\in C} T[S]=T\left[\bigcap_{S\in C} S\right]$ and $\bigcap_{S\in C} T[S]=T\left[\bigcup_{S\in C} S\right]$
> 3. What is the supremum of the collection of all function types? What is its infimum?

