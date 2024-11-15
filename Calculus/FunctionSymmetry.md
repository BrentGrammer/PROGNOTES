# Function symmetry

- Relatively rare. Most functions are not Symmetric

### Even vs. Odd functions

- Even Function: flip the sign of the input, and the output remains the same
- Odd Function: flip the sign of the input and the output also flips in sign

### Even Function example

$f(x) = x^2$ <br>
$f(-x) = (-x)^2 = x^2$ <br>

$$f(-x) = f(x)$$

- Multiplying the input by -1 gives the same result as the original input
  - Cosine is an even function

### Odd function example

$f(x) = x^3 -4x$ <br>
$f(-x) = (-x)^3 - 4(-x)$ <br>
$$f(-x) = -f(x)$$

- The result of multiplying the input by -1 gives us the result of the original function (without multiplying the input by -1) multiplied by -1

  - Sine is an odd function

### The Geometry of Function symmetry

- Draw vertical line at the x-axis = 0 tick
- In Even Functions (i.e. $y=x^2$ and $y = \cos(x)$), The function shape is mirrored across the line
- In Odd Functions (i.e. $y=x^3$ or $y=\sin(x)$), the function trajectory is not mirrored across the line
  - If you draw a horizontal line at y-axis = 0, double flipping an odd function does show you a mirroring effect (??)
    - See [video](https://www.udemy.com/course/pycalc1_x/learn/lecture/33947250) at timestamp 14:17
- **Non-symmetric/Asymmetric Functions** are not the same no matter how you flip them on the plot (i.e. $y=e^x$ or $y=\sin(x + \cos(x)^2)$)

### Importance of Symmetry in Functions

- Even and Odd functions have special properties that are relevant for derivatives and in particular, integrals.
  - Knowing whether a function is odd or even helps you compute the Integral of that function

### Any Function can be decomposed into Symmetrical Functions

- Any function (including Asymmetric Functions) can be decomposed into _the average_ of two other symmetric functions (one even, one odd):
  $$f(x) = {{f_e(x) + f_e(-x)} \over 2} + {{f_o(x)-f_o(-x)} \over 2}$$
- Hidden inside every function is two symmetric functions that combine to create a Non-symmetric function
