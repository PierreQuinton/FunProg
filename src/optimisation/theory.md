# From optimization to auto-differentiation

### Motivation: Machine Learning

In traditional programming, we give the computer rules and data to get an answer. In Machine Learning (ML), we give the computer the data and the answers, and it figures out the rules.

This shift allows us to solve problems that are too complex for manual rules, like recognizing a face in a photo or predicting the weather. In this course, we will follow the historical path of researchers: starting with simple math and building up to systems that can learn patterns.

### Warm-up Exercise: Finding the Minima

Before we can teach a computer to learn, we need to understand how to find the "best" version of something. One way to define "best" is as the minimum value of an error function.

> Exercise 1: Find the value of x that minimizes the following functions:
> 1. $f(x)=x^2$
> 2. $f(x)=x^2−4x+4$
> 3. $f(x)=ax^2+bx+c$ (where $0<a$)

To solve this, you likely used the derivative: set it to zero ($f'(x)=0$), and solved for $x$. This is a fundamental rule: a smooth function can only reach its minimum at a point where the slope is perfectly flat, or in other words, a point at which the derivative is null.

### The Foggy Mountain Problem (Gradient Descent)

Solving $f'(x)=0$ works great for simple polynomials. But in the real world, ML functions are so complex that we cannot solve them algebraically.

Imagine you are standing on a mountain in a thick fog. You want to reach the valley (the minimum), but you can only see the ground beneath your feet. What do you do? You feel the slope with your foot and take a small step in the opposite direction of the upward slope.

This idea can be translated into a mathematical statement: We can go some small step in the oposite direction to the derivative. If a function $f:\mathbb R\to\mathbb R$ is smooth (or at least continuously differentiable), we can approximate it locally with a straight line (it tangeant):

<!--math-->
$$
f(x+y)\approx f(x)+f'(x)⋅y
$$
<!--endmath-->

This is called the first order Taylor approximation of $f$ at $x$, it gets more precise as $y$ gets small.

If we want to decrease $f(x)$, we should pick a step y that makes the result smaller than $f(x)$. Let’s pick $y=−\lambda f'(x)$, where $\lambda$ is a tiny positive number called the *learning rate*.

Substituting this $y$ into the Taylor approximation, we get
<!--math-->
$$
f\big(x−\lambda f'(x)\big)\approx f(x)−\lambda \big(f'(x)\big)^2
$$
<!--endmath-->
Unless $f'(x)$ is zero, $\big(f'(x)\big)^2$ is always positive, and so we are guaranteed to subtract a value from $f(x)$, thereby decreasing it!

Of course this is an approximation and so the previous statement could be false, there is a compromise between for picking the right $\lambda$:
If $\lambda$ is too small, you take tiny baby steps and it takes forever to reach the minimum.
If $\lambda$ is too large, the approximation will be wrong, and we might take too big step that can result in increasing the function!

Before we move into higher dimensions, there is one catch to our Foggy Mountain strategy. So far, we have looked at parabolas, which have exactly one bottom. But what if the mountain range has many valleys?

A Global Minimum is the absolute lowest point on the entire landscape, the deepest part of the ocean. A Local Minimum, however, is just the bottom of a small puddle or a higher valley. Because our strategy only looks at the ground right beneath our feet, it is shortsighted. If you start your descent near a small dip, you might get stuck there, thinking you've reached the bottom, while the true Global Minimum is just over the next ridge. In Machine Learning (and in real life), we are always trying to find the absolute best solution, but sometimes our computer gets stuck in these local traps.

You may have heard that some modern models have hundreds of billons of parameters, or even trillions. Our function $f:\mathbb R\to\mathbb R$ has just one.

We typically want to have a function $f:\mathbb R^n \to \mathbb R$, where $n$ can be quite large. The logic stays the same, but we use the gradient $\nabla f(x)$ of $f$ at $x$, which is just a vector of all the derivatives.

The Taylor approximation of order $1$ at $x$ is approximation becomes:
<!--math-->
$$
f(x+y)\approx f(x)+\nabla f(x)\cdot y
$$
<!--endmath-->
Where the $\cdot$ indicates that we are taking an inner product.

By taking a step in the oposite direction to the gradient, i.e. setting $y=-λ\nabla f(x)$, we get:
<!--math-->
$$
f\big(x−\lambda \nabla f(x)\big)\approx f(x)−\lambda~\big\|\nabla f(x)\big\|^2
$$
<!--endmath-->

Applying such a step iteratively (or a small modification of it actually) is how most AI is trained today.

### Fitting a Curve

The Goal: Find the coefficients $a$, $b$, and $c$ for a parabola $y=ax^2+bx+c$ that passes through three specific points.

Suppose there are real parameters $a_0$, $b_0$ and $c_0$ that we want to find. We have acces to them only through three distinct points of the parabola $(x_i, a x_i^2+b x_i+c)$ for $i=1, 2, 3$ and for some $x_1$, $x_2$, $x_3$ distinct.

1. Find an objective function $f:\mathbb R^3\to\mathbb R$ that maps $(a, b, c)$ to some value, and such that $f$ is minimized only at $(a_0, b_0, c_0)$.
2. For any $(a, b, c)\in\mathbb R^3$, compute its gradient $\nabla f(a, b, c)$.
3. Write a Python code, using `numpy`, that defines some $a_0$, $b_0$ and $c_0$, and the polynomial $p(x)=a_0 x^2+b_0 x+c_0$.
4. Define the three points $(x_i, y_i)$, where $y_i=a x_i^2+b x_i+c$, as well as some small positive $\lambda$ (for instance $0.01$).
5. Define your function $f$, as well as its derivative.
6. Start from a random guess $(a, b, c)$ and iteratively improve in a loop by updating with the rule $(a, b, c) \leftarrow (a, b, c)-\lambda \nabla f(a, b, c)$.
7. At the end of the loop, plot $p$, the three points and your final estimate $x\to a x^2+bx+c$.

How do they compare? Play with the learning rate $\lambda$ by setting it to very small (`0.00001`) or large values (`1`), what do you observe?

### Terminology

Before we continue, let's name the parts of the machine we are building. In research papers, you will see these terms constantly:
- Input: The raw data we give to the machine (in our case, the $x$-coordinates).
- Target: The ground truth or the correct answer we want the machine to learn for the corresponding inputs.
- Model: The mathematical structure we choose (e.g., a degree $2$ polynomial). It’s like a box with knobs we can turn.
- Parameters: The specific values of those knobs (our $a$, $b$, $c$).
- Output or prediction: The model's current guess based on the input and parameters.
- Loss Function or objective: A formula that calculates the distance between the Prediction and the Target. It tells us how unhappy the model should be.
- Learning Rate: The step size we take during the update.
- Number of iterations: the number of gradient descent steps we are doing.

Since we are going to reuse the code for the rest of the course, spend some time improving the naming of your code, and to properly define the levels of abstractions by defining the appropriate functions.


### Noise and the Trap of Overfitting

In the real world, data is noisy. If you measure the height of students, your ruler might be slightly off, or a student might be slouching.

Change the code from the previous part to add a random normal Gaussian noise to the labels. For instance, you can use `np.random.normal(scale=10, size=3)` to generate a vector of size `3` of Gaussian random variables with standard deviation `10`.
Try running several times the fit, what do you observe?

Generalize your loss such that it accepts more data points (pairs of input/output). Try augmenting the number of sampled points you train on (the noise should be independent).
What do you observe?

Generalize your model such that it can be any degree `n` polynomial, and where you can parametrize `n`. Try augmenting the degree of the model. What do you observe?

---

# Auto-Differentiation: The Chain of Command

### The Problem with Manual Calculus

In the first part of the lab, you computed the gradient $\nabla f(a, b, c)$ by looking at the function as one big block. It worked, but it was tedious. If we decided to change our model from a parabola to a neural network, we would have to start our math from scratch. Worse than that, there is almost no chance we would get the derivative correct if differentiate by hand some very complicated model.

To fix this, we need to realize that our objective function is not one big blob, but a **composition** of simple steps. And the derivative of such an object can be obtained easily.

### Deconstructing the Loss Function

Let's look at the construction we built for our parabola fitting. We can break it down into three distinct stages:

1.  **The model ($f$):** We take our parameters $\theta$ and generate a vector of predictions.
<!--math-->
$$
\begin{align*}
f(x, \theta) = \begin{bmatrix} \theta_k x_1^k + \cdots + \theta_1 x_1 + \theta_0 \\ \vdots \\ \theta_k x_n^k + \cdots + \theta_1 x_n + \theta_0 \end{bmatrix} = \hat{\mathbf{y}} \in \mathbb{R}^n
\end{align*}
$$
<!--endmath-->
1.  **The error ($g$):** We compare these predictions to our targets $y_i$ by calculating the squared difference for each point.
<!--math-->
$$
\begin{align*}
g(\hat{\mathbf{y}}) = \begin{bmatrix} (y_1 - \hat{y}_1)^2 \\ \vdots \\ (y_n - \hat{y}_n)^2 \end{bmatrix} = \mathbf{e} \in \mathbb{R}^n
\end{align*}
$$
<!--endmath-->
1.  **The averrage ($h$):** We condense those individual errors into a single "loss" value (the Mean).
<!--math-->
$$
\begin{align*}
h(\mathbf{e}) = \frac{1}{n} \sum_{i=1}^n e_i = \mathcal{L} \in \mathbb{R}
\end{align*}
$$
<!--endmath-->
The entire training process is just finding the derivative of the composition: $\mathcal{L}(\theta) = (h \circ g \circ f)(\theta)$.


### The Chain Rule

In one dimension, if you have two functions $h$ and $g$, the derivative of their composition is:
<!--math-->
$$
\begin{align*}
(h \circ g)'(x) = g'(x) \cdot h'\big(g(x)\big)
\end{align*}
$$
<!--endmath-->
In Machine Learning, we deal with vectors. The derivative becomes a matrix (the Jacobian), and the multiplication is matrix multiplication. We call this the **Vector-Jacobian Product (VJP)**.

For the loss $L(\theta)$ defined above, this yields the following chain rule:
<!--math-->
$$
\begin{align*}
\underbrace{\frac{\partial \mathcal{L}}{\partial \theta}}_{1 \times k} = \underbrace{\frac{\partial \mathcal{L}}{\partial \mathbf{e}}}_{1 \times n} \cdot \underbrace{\frac{\partial \mathbf{e}}{\partial \hat{\mathbf{y}}}}_{n \times n} \cdot \underbrace{\frac{\partial \hat{\mathbf{y}}}{\partial \theta}}_{n \times k}
\end{align*}
$$
<!--endmath-->


### The Vector-Jacobian Product (VJP)

Notice the order of operations. We start with a row vector (the gradient of the output) and multiply it by a matrix (the Jacobian of the local step).

This is the main ingredient of auto-differentiation. We don't actually need to compute the full, giant Jacobian matrices (which could be billions of entries in a real model). We only need to know how to multiply a vector by that matrix.

Each step is a simple propagation of the gradient. This is why we call the main algorithm for propagation of the gradient the backpropagation algorithm.

## Scaling Up: Autodiff in the Real World

In the libraries **PyTorch**, **JAX**, or **TensorFlow**, are provided tools for applying such rules in order to formally compute the derivative of any computations. When you write mathematical operations in these libraries, they don't just calculate the answer; they also build a graph of every operation you performed. When you call for the gradient, they travel accross this graph backward, applying the Chain Rule (VJP) at every step.

The only difference is that these libraries are written in optimized C++ and CUDA, allowing them to handle billions of parameters across many of GPUs simultaneously.

---

### Porting to PyTorch

It is time to throw away our manual derivative functions and let the engine do the heavy lifting. We will now port our parabola-fitting experiment to **PyTorch**.

#### Setup
If you haven't already, install PyTorch in your environment:
```bash
pip install torch
```

#### From Arrays to Tensors

In PyTorch, we don't use `numpy.array`; we use `torch.Tensor`. They behave similarly, but `Tensor`s have the special ability to track their own gradients.
You can create those for isntance with
```python
import torch

x_train = torch.tensor([1.0, 2.0, 3.0])
y_train = torch.tensor([2.0, 8.0, 18.0])
```

#### Parameters and `requires_grad`

To tell PyTorch which variables we want to optimize, we must set the flag `requires_grad` to `True`. This tells the engine: Keep track of every operation involving this variable so I can compute its gradient later.
```python
theta = torch.randn(3, requires_grad=True)
```

#### The Optimizer

Instead of manually updating our parameters with `theta -= lambda * grad`, we use an optimizer. It handles the update logic for us. The simplest one is `SGD` (Stochastic Gradient Descent):

```python
optimizer = torch.optim.SGD([theta], lr=0.01)
```

#### The Task: The Modern Training Loop

Rewrite your previous lab code using PyTorch. Your loop should follow this standard learning pattern:
1. Zero the gradients: PyTorch accumulates (adds) gradients by default. You must clear the old ones at the start of every loop: `optimizer.zero_grad()`
2. Forward Pass: Write the math normally. PyTorch builds the graph automatically: `preds = theta[0]*x**0 + \theta[1]*x**1 + ...`,  `loss = torch.mean((preds - y_train)**2)`
3. Backward Pass: This is the magic line. It triggers the VJP chain described above: `loss.backward()`
4. The Step: The optimizer nudges the parameters in the direction of the gradient: `optimizer.step()`
