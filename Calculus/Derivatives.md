# Derivatives

See [Python Notebook](./derivatives.ipynb)

- The slope of the line of a function as the Limit of change approaches 0

### Note on Differentiation vs. Derivates

- Derivative: The instantaneous slopes (i.e. at each point)
- Differentiation: The process and the technique of getting the derivative

## Notation

- the Delta greek letter represents a change in some quantity:$\Delta x \over \Delta y$
  - or it's lowecase variant: $\delta x \over \delta y$
- Leibniz and Lagrange are the most common forms

### Leibniz notation

- df = change of function and sometimes the function is written outside the ratio notation as well: $${dy \over dx} = {df \over dx} = {d \over dx}f(x)$$
  - Higher order derivative notation: ${d^2y} \over {dx^2}$
- Chain Rule: $${dy \over dx} = {dy \over du} \times {du \over dx}$$

### Lagrange Notation

- More compact than Leibniz (f prime of x is the derivative) $$f'(x) = f' = fx$$
- second derivative or partial derivatives: $f'' = fxx$

### Newton Notation

- Simple - use a dot on top of the dependent variable (second derivate uses double dot)
- Commonly used to notate derivatives of physical forces over time (physics)
  $$\dot{y} \quad \ddot{y}$$

### Euler Notation

- Least commonly used, is a Capital D in front of the function:
  $$Df = Df(x) \quad D^2f \text{(second derivative)}$$

## The Slope of a Line

- **A Ratio** of the distance along the y-axis between two points over the distance along the x-axis. That ratio is the **Slope**.
- The change in `y` (output) over the change in `x` (input)
  - How much the dependent variable $y$ changes given some change in the independent variable $x$
- A higher ratio/number means that the slope is steeper, a smaller ratio means that the slope is less steep and more gradual

### Line function

- A line expressed as a function is:
  $$f(x) = mx + b$$
- $m$ is the slope parameter and $b$ is the `Intercept`

#### The Intercept: Where the line crosses the y-axis when input $x = 0$ in the function.

- The Intercept is unimportant for the Derivative - we only care about the $m$ slope parameter

### Computing the Slope parameter $m$

- The change in the $y$ axis values normalized by the change in the $x$ axis values

  - Take the difference between the y-axis of 2 points on a line and divide it by the difference of the x-axis coordinates for those points
    $$m = {{y_2 - y_1} \over {x_2 - x_1}} = {\Delta y \over \Delta x}$$

- You will also see the slope formula as the change of a function where $x$ plus a small change in $x$ minus the function with just $x$ over the change in $x$:
  $$m = {{f(x + \Delta x) - f(x)} \over \Delta x}$$
- or using $h$ in place of $\Delta x$:
  $$m = {{f(x + h) - f(x)} \over h}$$

#### Special Slope Properties of Straight Lines

- **NOTE:** No matter what $x$ value or $h$ you use for getting the slope of a straight line, you will always get the same slope result. A property of straight lines is: the slope anywhere is the slope everywhere
- The global slope is the same as the local slope (of a line segment)
- These properties hold true for the derivative of straight lines as well

### The Slope as it relates to the Derivative

- If we continue to chop up a portion of a line between two points into smaller and smaller line segments to get the Limit as the distance on the x-axis between those segments goes to 0
- The distance between two points along the x-axis $\Delta x$ as it gets smaller and smaller arbitrarily close to $0$ without actually being $0$ (then we would have ${\Delta x \over \Delta y} = {0 \over 0}$)
- At the limit as the segments get smaller and smaller towards 0 length (but not 0), we have a **slope series** (i.e. a vector of slopes for each chopped up line segment) - this is the Derivative
  - The slope series becomes the derivative when the segments are so numerous that the distances between them is almost 0

## The Derivative

- The derivative is **the Limit** as a change in the input $h$ goes to $0$
  - In other words, as the change of $x$ is an "infinitesimal" or very close to $0$
- Or the Slope of a line segment as the x-axis distance (x coords of the two end points) goes to $0$
  - How the function behaves or what it moves towards as $h$ gets closer and closer to $0$
- (Note: when $h$ goes to $0$ you have a undefined limit since you cannot divide by $0$ and need to use techniques to do differentiation to get around this)
  $${dy \over dx} = \lim_{h \to 0}\left[{{f(x+h)-f(x)} \over h} \right]$$

### Empirical vs. Analytical Derivative

- "Discrete Derivative" or Difference vector - this is not the same as the analytical derivative which you would write out on a chalkboard, for ex.
  - Based on a discrete difference between a point and a previous point, not an analytical "pure" derivative, but a empirical derivative
  - in Numpy: `np.diff(fx) / dx` - run function input diffs and scale by the change in x where dx is a paraterized step size - see [Notebook](./derivatives.ipynb)
- The smaller and closer the `dx` step size parameter is to zero, the closer the empirical derivative gets to the actual analytical derivative

### Slope vs. Derivative

- "Slope": when $\Delta x$ is relatively large
- "Derivative": when $\Delta x$ is infinitesimal and very tiny and arbitrarily close to $0$ without actually getting to $0$ (i.e. infinitesimal)
  - **The Slope gotten from the Derivative can change at each infinitesimal change of input $dx$**

### Getting around dividing by 0

- Use algebraic expansions like the distributive property to expand the equations out and cancel out terms to help get a solution (as the limit goes to 0)
- **The Distributive Property:**
  For any number a and terms b and c:
  $$a(b + c) = ab + ac$$
  This rule applies to any number of terms inside the parentheses. For instance:
  $$a(b + c + d) = ab + ac + ad$$

#### Expansion:

Algebraic expansion for the func: $(2(x+h) + 5) - (2x+5)$:

1. Distribute the 2 in the first parenthesis: $(2x + 2h + 5) - (2x + 5)$

Now we have removed all nested parentheses.

2. The next step is to subtract the second set of parentheses from the first.

When subtracting expressions in parentheses, we change the operation for all terms inside the second parenthesis. In this case, subtraction becomes addition, and addition becomes subtraction:$(2x + 2h + 5) + (-2x - 5)$

3. Now we can remove the parentheses completely:2x + 2h + 5 - 2x - 5

4. Finally, we combine like terms:

The $2x$ and $-2x$ cancel out.
The $5$ and $-5$ cancel out.
The $2h$ remains and is the final simplified expression.

#### Expanding binomials - For any binomial $(a + b)^2$:

This expansion is also known as the "FOIL" method when applied to multiplying two binomials, as $(a + b)^2$ is equivalent to $(a + b)(a + b)$.

### Example computing the Derivative for $x^2$

$$f(x) = x^2$$
$${dy \over dx} = \lim_{h \to 0}\left[{{(x+h)^2 - x^2} \over h} \right]$$

- Expand algebraically with the goal of getting around having to divide by $0$:
  $$= \lim_{h \to 0}\left[{{x^2+2xh+h^2-x^2} \over h} \right]$$
- $x^2$ cancels out, then factor out $h$:
  $$= \lim_{h \to 0}\left[ {{h(2x+h)} \over h} \right]$$
- $h$ cancels out:
  $$= \lim_{h \to 0}\left[ 2x + h\right]$$
- We now don't have to worry about divide by $0$, just use the plugin method by setting $h$ to $0$:
  $${dy \over dx} = 2x$$
- The slopes of the tiny line segments change for different values of $x$ (as opposed to a straight line where the derivative and slope is constant)
  - We leave $x$ as a variable because we want to allow for different slope values depending on $x$
  - The slope of the function when $x=0$ is $0$, when $x=1$, the slope is $2$, etc.

### Differentiation is a LINEAR Operation

- Scalar multiples and additive terms in a function can be differentiated separately and summed to get the derivative of the entire function (the same result if you differentiated the entire function and not the separate terms individually).
  - You can differentiate the terms with the independent variable (i.e. $x$ for example) and pull out the constants
- You can take the differentiation of separate additive terms in a function and add them all together to get the derivative of the entire function
- Example: Scalars $a$ and $b$ are scalar multipliers of two functions $f(x)$ and $g(x)$ which are terms in a whole complete function we are differentiating:
  $${d \over dx} \left[af(x) + bg(x) \right]$$
- Because Differentiation is linear, we can differentiate the two function terms in the original function separately, then multiply those DERIVATIVES of the two functions by the scalars $a$ and $b$, take the sum and the result is exactly the same as getting the derivative for the entire function:
  $$af'(x) + bg'(x) = {d \over dx} \left[af(x) + bg(x) \right]$$

#### Multiplier scalars with the Linearity Property of Differentiation

- $a$ is a constant and $x^2$ is a term in the entire function.
- We can take the derivative of the term being multiplied by the constant and multiply the scalar constant by it to arrive at the same result as the derivative for the entire function
  $${d \over dx}\left(ax^2\right) = a\left({d \over dx}x^2\right)$$

## Geometry of Derivatives

### Secant and Tangent lines

- Descriptions of straight lines that pass through functions
- Secant line: passes through two points in a function (that are not infinitessinally close to each other)
- Tangent line: a line that passes through two points in a function which are infinitessimally close to each other (looks like it's grazing one point of the function graph)

### Geometric definition of a Derivative

- The slope of the Tangent Line at some point $x$ on a function $f(x)$
  - The tangent line passes through two points that are infinitessimally close to each other on the x-axis
  - Or the tangent is what you get when you take a Secant Line starting at $x$ and crossing through some other point on the function graph and you bring the distance of the points smaller and smaller to 0 (The limit as the distance $\Delta x$ approaches 0)

## Interpreting Derivative Plots

- **Shows the slope of a function at each point**, not the value (output) of the function - it shows you how the function is CHANGING
- A Derivative plot is a plot of the Tangent Line (a pair of infinitesimally close points on the function) at each x-axis point
- Two features to look for in Derivative Plots:

  - The sign of the derivative (is it positive or negative) tells you where the function is going up or going down
  - Where does the derivative cross 0? Those are critical points where the function changes direction. Indicates that the function is doing something qualitatively different.

- Derivative plot of sin (note that when the y value of the derivative plot is negative, the sin function is sloping down, and when positive it slopes up)
  <br>
  <img src="./sinderivativeplot.png" width="400" height="auto" />
  <br>

### Example of a Derivative plot that is more complicated

- For the function $x^3 - x^2$, the slope of the function goes up and down and back up
- The derivative plot for this function looks like $x^2$, but you should interpret it as showing that the slope of the function is positive to start with, negative and then positive again
  - Note where the derivative plot crosses 0 on the y-axis at two points - these represent changes in direction of the function
    <br>
    <img src="./derivativeplot.png" width="400" height="auto" />
    <br>
- The derivative plot of $ln(x)$ - The first is the plot of the function and the plot below is the derivative plot.
  - The derivative plot shows us that the function is always going up (the derivative is always a positive number - y-axis on derivative plot)
  - The derivative plot also shows that the function starts with a high slope and then the slope starts decreasing so it is less and less steep
    <br>
    <img src="./logplotderivative.png" width="400" height="auto" />

## Diffentiating Polynomials

- Polynomials are really easy and fast to compute the derivate for

### The Power Rule

- Workds for any real number except when $r=0$
- To get the derivative of a polynomial, take the exponent $r$ and put it in front of the coefficient $c$ as a multiplier and subtract 1 from the exponent
  - The exponent comes down as a coefficient that multiplies any existing coefficient
    $$f(x) = cx^r \quad \rightarrow f'(x) = rcx^{r-1}$$
- Example: $f(x) = x^2 \quad \rightarrow f'(x) = 2x^{2-1}$
- **NOTE**: This rule only applies to simple polynomials, not composite functions (where you have exponents and sqaure roots or sin functions in other terms, etc.)

### Differentiating a polynomial with multiple terms:

- NOTE: Derivative of a constant is always 0 (here the constant is the term $10$), the derivative of $x^1$ is $1$ for the term $x$
  - side note: The 12x^3 and 7.5x^2 cannot be simplified further because they are not like terms (do not have the same exponent)
    $$\frac{d}{dx}(3x^4 + 2.5x^3-7x^2+x+10) = 12x^3 + 7.5x^2 -14x + 1 + 0$$
- if you have more complicated terms, here $e^{\pi}$ and $\pi^e$, that do not involve $x$, then treat them as constants:
  $$\frac{d}{dx}\left(e^{\pi}x^2-\pi^e x^4\right) = 2e^{\pi}x-4\pi^e x^3$$
- For a trinomial multiplied by a binomial, use the distributive property
  $$
  2(x^2 + h^2 + 2xh)(x + h) \\
  \text{To distribute (x + h), we multiply each term inside the first parenthesis by x, and then by h, and add the results:} \\
  (x^2) * x = x^3 \\
  (x^2) * h = x^2h \\
  (h^2) * x = xh^2 \\
  (h^2) * h = h^3 \\
  (2xh) * x = 2x^2h \\
  (2xh) * h = 2xh^2 \\
  \text{Final solution:} \\
  x^3 + x^2h + xh^2 + h^3 + 2x^2h + 2xh^2
  $$

### Parity of Polynomial Derivatives

- Even polynomial functions always have odd derivatives (the number in the exponent due to $n-1$ for it in the Power Rule)
  $$f'x^2 = 2x^1$$
- Odd polynomial functions always have an even derivative
  - Odd polynomials function values are always increasing! (they can start negative, but as x increases, y always goes up)
  - Their derivatives everywhere along the function are non-negative (could include 0, but all other slopes are positive)
    $$f'x^3 = 3x^2$$

## The Derivatives of Sin and Cosine

- The derivatives of cosine and sin are cyclic and go back and forth around a cycle of 4 differentiations
  - $f'\cos(x) = -\sin(x)$
  - $f'-\sin(x) = -\cos(x)$
  - $f'-\cos(x) = \sin(x)$
  - $f'\sin(x) = \cos(x)$
- Trick to remembering: "Cosine to sin switches the sign" (derivative of cosine is negative sin)
  - The derivative of sin keeps the same sign
- see exercise in [Notebook](./derivatives.ipynb) for how to cycle through the differentiations with sympy

#### Are Inverse Trig functions also cyclic?

- i.e. arc cosine, or $\cos^{-1}(x)$, starting the cycle is NOT cyclic like the trig functions above. The cycles only apply to cos and sin

## Derivative of absolute value, Square Root, log and exp Functions

### The derivative of Absolute Value Function

- Surprisingly, the abs value function has a complicated derivative
  $$f(x) = |x|$$
- It is a piecewise function with a non-differential point in the middle
  - if $x$ is negative, multiply it by -1 to get it negative, if positive it is just $x$
    $$
    = \begin{cases}
        -x \text{ if } x < 0 \\
        x \text{ if } x \ge 0
    \end{cases}
    $$
- The derivative needs to also be a piecewise function.
  - The derivitive with respect to x if x is negative is -1, if positive, +1
  - **When $x=0$ the derivative is undefined**. There is infinite tangents you could place at the tangent line where x is 0 since the function abruptly goes in the opposite direction (so the derivative plot has a discontinuity there)
  - Note that the derivative of the absolute value function is not technically the Signum (sign function) since there is a discontinuity at x=0, it is used for brevity and ignores that specific case.
    $$f'(x) = \text{sgn}(x)$$
    $$
    = \begin{cases}
          -1 \text{ if } x < 0 \\
          1 \text{ if } x \ge 0 \\
          \text{d.n.e.} \text{ if } x = 0
      \end{cases}
    $$

### The derivative of the Square Root

- You can rewrite the square root function as exponentiated $x$ to $1/2$ and then use the power rule to get the derivative
  - (power rule = $cx^r \rightarrow rcx^{r-1}$)
    $$f(x) = \sqrt{x} = x^{1/2} \quad \rightarrow f'(x) = {1 \over {2\sqrt{x}}} = 1/2x^{-1/2}$$

### The derivative of the Natural Log

- Note: all logarithms regardless of their base are 0 when $x=1$
  - The log of $0$ is negative Infinity
  - The log of a negative number is undefined in real number terms (it is a complex number)
  - The Natural Log uses the mathematical constant $e$ (approximately $2.71828$) as its base
    - side note: $log_e(e) = 1$
- The log function always go up, so the derivative is always positive. It starts extremely large when $x$ is close to $0$ and gets smaller and smaller as $x$ gets further away from $0$

#### The derivative for the Natural Log:

$$f(x) = \ln(x) \quad \rightarrow f'={1\over x}$$

#### The derivative for logs using other bases:

- The derivative for logs other than natural log is still $1/x$ but scaled by the base $B$
  $$f(x) = \log_{B}(x) \quad \rightarrow f' = {1 \over {x\ln(B)}}$$

### The derivative of exp $e$

- The derivative of the Natural Exponent $e^x$ is identical to $e^x$
  - This is a remarkable feature for $e$ that is **unique**. There is no other function that is it's own derivative! (except for $y=0$, but that can be expressed as a special case: $y=0e^x$)
    $$f(x) = e^x \quad \rightarrow f' = e^x$$


## Critical Points
- Special points on a function where the behavior changes in some significant way or is degenerate at that point
- Useful in optimization
- 