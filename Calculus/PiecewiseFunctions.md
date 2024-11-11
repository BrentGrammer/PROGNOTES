# Piecewise Functions

- [Python Notebook](./piecewisefunctions.ipynb)

- Applications in applied math and deep learning

## What is a Piecewise Function

- A function that comes in multiple different pieces
  - Each piece is a separate function with its own subdomain (the range of inputs)
  - It has a rule (operation to perform on the input resulting in an output) and a subdomain (the range of inputs can be expressed as a boolean condition, i.e. `when x > 0`)

### Example of a piecewise function

- Each row is called a "case" (i.e. a piece of the function)
- 2 columns:
  - the first column describes the function (the rule that is applied to the input)
  - the second col defines the domain (range of inputs) for that piece/function
- Each piece (row) can be inclusive or exclusive

$$
f(x) = \begin{cases}
    x^2, & \text{if } x < 0 \\
    \sin(x), & \text{if } 0 \leq x < \pi \\
    x+1, & \text{if } x \geq \pi
\end{cases}
$$

#### The absolute value function as a piecewise function:

$$
f(x) = \begin{cases}
    x & \text{when } x \geq 0 \\
    -x & \text{when } x < 0
\end{cases}
$$

- The first case applies the rule: $x$ (just return $x$), when the condition that $x > 0$ holds
- The second case applies the rule: $-x$, when the input $x$ is less than 0 (so $x$ becomes positive when the input is negative, i.e. $-(-x)$)

#### ReLU (Rectified Linear Unit) as a piecewise function:

- Used in Deep Learning to introduce nonlinearities
- Note that each of the pieces are linear themselves (though the entire function is nonlinear)
  $$
  f(x) = \begin{cases}
      0 , & x < 0 \\
      x , & x \geq 0
  \end{cases}
  $$
