# Inverse Functions

- [Python Notebook](./inversefunctions.ipynb)

A category of functions that negates or "undoes" the tranformation of a variable done by another function.

### Definition

$g(x)$ is the inverse of $f(x)$ if $g(f(x)) = x$

- A function is the inverse of another if it gives us back the original variable $x$ passed into the first (undoes the mapping/transformation the first function does on the input)

### Notation

- We use a -1 superscript to indicate a function is an inverse function:
  $$f^{-1}(f(x)) = x$$
  - **It indicates that the function is negating the transformation applied to the variable $x$**
  - Note this is not the reciprocal or notation of that though it is related
  - a -1 in the exponent inverts a number, ex. $3^{-1} \times 3 = {1 \over 3} \times 3 = 1$
    - $1 \over 3$ negates the $3$ and gives us back $1$, the multiplicative identity number
    - So, for numbers, the inverse function is the same thing as the reciprocol, but usually not the case for functions

### Example

$$f(x) = 2x + 3$$
$$g(x) = {x-3 \over {2}}$$
$f(g(x)) = x$
$g(f(x)) = x$

- The two composite functions are commutative
  - In $g(f(x))$, $f(x)$ transforms the variable $x$ passed into $g$ into some other value, and $g$ undoes the transformation and puts it back to $x$

## Computing the Inverse function

1. Express the function as $y = \text{definition}$
1. Solve for $x$
1. Swap $x$ and $y$ to get the inverse function definition

Note: in practice, we just use Sympy to help us compute the inverse function

### Examples

$$f(x) = 2x + 3$$

- Write as y = <br>
  $y = 2x + 3$
- Solve for x: <br>
  $y-3=2x+3-3$ <br>
  ${(y-3) / 2} = x$ <br>
- Now swap x and y to get the inverse function:
  $$(x-3)/2 = y = f^{-1}(x)$$

### Inverse of a sin function

$$f(\theta) = \sin(2\pi\theta)$$

- (arcsine inverts a sin function) <br>

  $\arcsin(y) = 2\pi\theta$ <br><br>
  $\arcsin(y) / 2\pi = 2\pi\theta$ <br><br>
  $\arcsin(\theta) / 2\pi = f^-1(\theta)$ <br><br>

### Another Example o9f Computing an Inverse function

$$f(x) = 3x^2 + 4$$

$y-4 = 3x^2$ <br><br>
${{y-4} \over 3} = x^2$ <br><br>
$\sqrt{{y-4} \over 3} = x$ <br><br>
$\sqrt{{x-4} \over 3} = f^{-1}(x)$ <br><br>

#### Notes on the above function/inverse

- The domain of the original function is infinity
- The domain of the Inverse is $x \geq 4$ (negative numbers under the square root give us a complex number)
- Also Note: The inverse of the above function is only for the positive lobe (not the whole domain of the original function, since we are only dealing with numbers above 4)
  - You can define **two different** inverse functions, one for the positive lobe and one for the negative lobe (parts of the domain) by adding a negative in front of the sqrt:
    $$-\sqrt{{x-4} \over 3} = f^{-1}(x) \quad\text{(inverse fn for the Negative lobe)}$$
- Note that you can plot these functions

### Note on the domains

#### **The domain (output) of the inverse function corresponds to the domain of the original function - they are the same!**

- The domain (range of output) of the original function is the same as the Range (allowable inputs) of the Inverse
- The Range of the original function is the same as the Domain of the Inverse function.

$$f(x) \quad\quad f^{-1}(x)$$
$$\text{Domain} \longrightarrow \text{Range}$$
$$\text{Range} \longrightarrow \text{Domain}$$

### Functions WITHOUT an Inverse

$$f(\theta) = 2\theta\sin(2\pi\theta)$$

- There is no inverse to this function that you can compute
  - It is impossible to isolate $\theta$ (the input $x$) on one side of the equation
- **There are many functions that do not have an inverse**
