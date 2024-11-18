# Functions

- An expression or set of rules that maps one variable or set of variables onto another variable

$$y = f(x)$$

- y is called the dependendent variable (it's value depends on `x`)
- x is called the independent variable
- the function `f` maps a value of variable `x` onto values of variable `y`

### Graphing functions

- See [Python Notebook](./plotAFunction.ipynb)

- Typically you have the independent variable on the x-axis and the dependent variable on the y-axis
- **You cannot have more than one value of y for each value of x**
  - You can have multiple x values with the same y value, but not vice versa
  - A circle on a graph is NOT a function since at the top and bottom of
    the circle there are two values of y for one point on the x-axis.
  - **Vertical Line Test** draw a vertical line anywhere on the graph and if it passes through more than one point, then the graph is not showing a technical function.
    - Extreme example: A vertical straight line on a graph is not a function and has a slope of infinity (it has multiple y values for the same x)
  - $f(x) = \sqrt{x}$ is not a function since a sqeare root can have positive and negative solution (this results in a double prong line on the graph which fails the vertical line test). You need to only consider or graph the principal (positive) solution of the square root or only use the negative solution.

### Constants

- The variable that is mapped onto by the function does not contain the independent variable: EX: $y = h(x) = \pi$ (the result is pi regardless of `x)
  - This would be a straight horizontal line along the y value of pi on a graph

### Domain and Range of a function

- Domain: Set of all possible values of input to a function
- Range: Set of all possible values of the output
- Trick to remember terms: x (input) comes before y (function output) in alphabet and D comes before R in the alphabet
- You can optionally restrict the domain or range (Notation: [.5,5.25])

#### Notation (3 ways to notate Domain and Range)

- Intervals: $D = ( -\infty,+\infty )$ - represent lower and upper bound (exclusive of infinity means arbitrarily close to it)
  - For range example: $R = [ 0, 10 )$
    - square bracket means Inclusive boundary
    - parens indicate exlcusive boundary
- Inequality notation: $-\infty < x < \infty$
  - `<` or `>` mean exclusive boundaries
  - less than or equal to etc. mean inclusive boundaries
- Set builder notation: $D : \{ x | x \in \R \}$
  - first write the variable i.e. `x` for input (domain), and then the collection of all possible values of that variable
  - the pipe `|` means "given that" or "for" (in this case)
  - $\in$ means "element of" or that the value is in the set of the following value
  - the $\R$ means set of Real Numbers
  - if there are multiple boundaries you can use the union symbol ($\cup$): $(-\infty,0)\cup(0,2)$

## Linear vs. Nonlinear functions

- LINEAR: a function's graph is a straight line
- NONLINEAR: a function's graph is not a straight line **Has Curves**

### Linear functions

- You can simplify them algebraicly to:
  $$y = mx + b$$
- where `m` is the slope and `b` is the intercept
- Example: $y = 2x + 6$ or $xy = 3x^2 -4x$
- Another way to look at a linear function is: ${\Delta{y} \over \Delta{x}} = c$
  - for each change in `x`, the change in `y` is the same (`c` means Constant) - or, the ratio of change in output to the change of input is constant
  - see [video](https://www.udemy.com/course/pycalc1_x/learn/lecture/33947186#notes) at timestamp 5:39
- Side Note: Linear functions that do not pass through the origin (0,0 on a graph) are called **Affine Functions**
  - see [video] at timestamp 8:31

### Nonlinear Functions

- You can NOT simplify the function to: $y = mx+b$
- Example: $y = 3x^2 - 4$ or $y = 2\sqrt{\cos(x)} + 6$
  - NOTE: the nonlinearity comes from that which is applied to `x` (input)
    - $y = \sqrt{2}x + \cos(6)$ is a lenear function, the cosine and square root are nonlinearities, but they are not applied to `x` they are applied to constants (2 and 6)
    - IOW, the square root of 2 is still just `m` and the cosine of 6 is still just `b`
- ${\Delta{y} \over \Delta{x}} = c$ does not hold true for $y = x^2$
  - the change in the output from `x=2` to `x=4` is 12 (16($x^4$) - 4($x^2$))
  - the change in the input of `x=2` to `x=4` is 2 (from `x=0` up, the ratios of output change to input change are 4/2, 12/2, so not constant)
    - Note, careful with this method, there could be sub-domains (range of inputs) of nonlinear functions that are linear and it could look like it is linear when it is not when you look at a wider domain!
    - **Piece wise functions** - functions with linear and nonlinear parts
      - fuctions can have two or more pieces that are linear, but it cannot be represented as a linear mx+b function (this would be a nonlinear function that has linear components)

# Polynomial Functions

- Category of functions where you raise the independent variable (`x`) to higher powers and multiply by some coefficient.

### Notation

$$a_0 + a_1x + a_2x^2 + a_3x^3 + a_nx^n$$

- Take independent variable `x`
- Raise it to higher and higher powers
- Multiply it by some coefficient
- Sum all of the values together

### Shorthand notation

$$y = {\sum_{i=0}^n}a_ix^i$$

### The Intercept term

- NOTE: the first term $a_0$ is sometimes called the **Intercept**
- This is the value y (output) when the independent variable `x` = 0

## Order of Polynomials

- Order: $n$ is the highest power that `x` gets raised to is called the **Order** of the polynomial
  - it says the function is an `nth` order polynomial (i.e. a 3rd order polynomial if the highest exponent is 3)
  - Note that you don't need all the exponents in the function: $2x + x^3$ is a 3rd order polynomial
  - An nth order polynomial has $n+1$ coefficients (i.e. a 3rd order polynomial will have 4 coefficients, i.e. the numbers you multiply the independent variable by) because we are including the $x^0$
- **The highest power in a polynomial dominates and determines the behavior of the function**
  - Exceptions: When the coefficient (number multiplied by `x`) is tiny on the highest order relative to the coefficient of the lower powered term, then the lower power term will dominate the behavior when `x` is small.
    - But, as you zoom out, and x gets larger (on the x-axis), the highest power will eventually dominate
    - Example: $x + x^2 + 0.1x^3$

### Shapes of Polynomials

- see [video](https://www.udemy.com/course/pycalc1_x/learn/lecture/33947192#notes) at 3:11
- 0 order polynomial ($x^0$): A flat line (at 1 on the y axis, or if there is a coefficent the intercept is at whatever the coefficient is (coeffient x 1))

#### Even vs. Odd functions

- EVEN Fns: Even numbered order polynomials have a symmetric (`U`) shape where each side mirrors the other
  - Even ordered polynomials cannot be negative (negatives multiplied by each other even number of times always yields positive results)
  - Mirrored across the x = 0 line
- ODD fns: Odd numbered order polynomials have a more asymmetric (`S`) shape
  - Odd powered polynomials can be negative
  - mirrored, but are negative on one side
  - Note that they can appear to have more of a `U` shape if zoomed in on a smaller X axis domain, but if you zoom out, the `S` shape will emerge

## Arithmetic with Polynomials

### Addition/Subtraction

$$(3 - 5x + {5\over6}x^2 + 12.4x^3) + (2x + x^3) = 3 - 3x + {5\over6}x^2 + 13.4x^3$$

- With Addition: **You can only add terms if they are raised to the SAME power**
  - In the above example, -5 on the left expression and 2 on the right expression can be added together because they are both multiplied by `x` to the power of 1 (we get -3x)

### Multiplication

$$y^a \times x^a \times x^b = y^a \times x^{a+b}$$

- Use the **Law of Exponents**: When you multiply two base terms, then their exponents will sum
  - $x^a \times x^b = x^{a+b}$

### Rational Functions

- Referring to 'ratio' i.e. fractions
- A function that is defined by the ratio of two polynomials
  $$r(x) = {P(x) \over Q(x)} = { {\sum_{i=0}^n}a_ix^i \over {\sum_{i=0}^k}b_ix^i }$$
- Similar to rational numbers, but instead of numbers in the numerator and denominator, they are polynomial functions
  - You could think of it as a rational number where the numbers in the fraction (ratio) come from the polynomial functions for one specific value given the independent variable `x`

## Transcendental Functions

- A function that cannot be expressed by combining a finite number of terms algebraicly.
- Functions that just cannot be expressed through algebra or agebraic operations.
  - They "transcend" algebra

### Four types of common Transcendental Functions

- cos(x)
- sin(x)
- log(x)
- exp(x)

## Exponential and natural log Functions

### Exponential Function

$$e^x$$

or

$$exp(x)$$

- `e` is an irrational number (never ends, i.e. like pi)
- e = 2.178281828459045...
  - important to memorize the first few digits: 2.718
- the `x` could either be one variable or an entire expression: $e^{3x+\cos{(x)}}$ or $exp(3x+\cos{(x)})$

### Properties of the Natural Exponential function

- The range (output) is any positive real number from just above 0 to infinity
  - Always Positive
  - cannot actually equal 0 for any value of x (can only get arbitrarily close to 0)
- e^0 = 1
- e^1 = 2.718... (Euler's Number - an important constant in Math)
- if `x` = any positive number, the output is greater than 1
- if `x` is negative, any output is less than 1 and greater than 0
- As `x` gets larger, $e^x$ blows up to infinity and increases very rapidly
  - The derivative of $e^x$ is $e^x$
  - This is a unique property that the derivative of the function is the function itself!
- $e = \lim_{n \to \infty}(1 + \frac{1}{n})^n$ - as $n$ approaches infinity, the output of this function approaches $e$, or Euler's Number (2.718...)

### Calculating `e`

- Multiple ways to calculate `e` (based on geometric property, or desired deritivative property,etc.)
- One way to calculate it is: $$e = \lim_{n \to \infty}( 1 + {1 \over n})^n$$
  - limit as `n` goes to infinity with the expression following
  - `n` gets bigger and bigger and approaches infinity, and then we get the irrational number, `e`
  - `n` as it is smaller, is only a rougher estimate of `e` - as `n` gets larger, the error between the output and the actual value of `e` gets smaller.

### Natural Log

- Notation: $ln(x)$
- If `x` is negative or `x` = 0, the natural log of `x` is undefined.
- The natural log goes to $-\infty$ as `x` approaches 0
  - you can take the natural log of a negative number and it will return a complex number value.
- The natural log of `x` goes to $\infty$ as `x` goes to $\infty$
  - \*Unike the natural exponent, as `x` gets larger and larger in the natural log, the output's rate of increase gets slower and slower
    - it always increases and never asymptotes, but goes up more and more slowly as x increases

### The natural log is an inverse of the natural exponent

- One function negates or cancels out the other
  $$\ln(e^x) = x$$
  $$e^{\ln(x)}=x$$
- When you embed one into the other, you just get back `x` whatever is in the exponent
- The domain and range are different, though:
  - The domain of $\ln(e^x) = x$ is $D(x \in \R), R(y \in \R)$
  - The Domain is the entirety of Real Numbers (all numbers from negative to positive can be an input)
  - The Range is the same (all numbers from negatife infity to positive infinity can be the output)
- The domain/range of $e^{\ln(x)} = x$ is $D(x > 0), R(y > 0)$
  - The Domain is the entirety of Real Numbers (all numbers from negative to positive can be an input)
  - The Range is the same (all numbers from negatife infity to positive infinity can be the output)
  - the natural log function is defined only for values that are greater than 0
    - The input as `e` can be negative, but the input `x` into the natural log function (in the exponent) cannot be negative
    - The output is always going to be a positive number
- The Domain and Range of the inverse equations shown above are different, so that means that the natural log and natural exponential are inverses only within their specific domains.

### Notes on log functions

- Logarithms are inverses of power functions (exponential functions)
  $$x = b^y$$

$$y = log_b(x)$$

$$b > 0$$

- log inverts an exponential or is what is defined in the exponent of a function
- When you set the base `b` to be the natural to be the natural exponent `e`, then you get what is the Natural Logarithm
  - i.e. Given $x = e^y$, then $y = log_e(x)$
  - or conventially: $\ln (e^x) $

# Intermediate Value Theorem

A function that is continuous in [a,b] has all values between $f(a)$ and $f(b)$ are present at least once in that function

### Definition of the Intermediate Value Theorem

- For any output number on the y-axis between two points - $f(a)$ and $f(b) on the y-axis$ - there is a corresponding x-axis coordinate (number) that produces that output which is between points/numbers $a$ and $b$ on the x-axis.
- **Interval**: the range of two points on the x-axis we are considering, notated in brackets, i.e. $[ 2,4 ]$
  - Can also be thought of as a subdomain for particular problems ( a range of inputs )
- The function must be continuous for the interval for the theorem to hold

### Example

- $x^2$: Any number between 4 and 16 on the y-axis has a corresponding x-axis value between 2 and 4
  - i.e. for the y-axis 9, the value to produce $f(x)$ where $x = 0$ must be between 2 and 4 on the x-axis (it is 3)

### Exceptions to the theorem - Discontinuities

- Any function with a discontinuity can break the Intermediate Value Theorem
  - A Piecewise function can violate this rule by having a jump discontinuity, or any discontinuity
- **The function must be continuous within the specified interval**

### Use cases

- Useful for finding whether a polynomial equation has a certain set of solutions
  - (i.e. determining the roots - the solutions to $x$ when you set the equation to 0)
  - $0 = x^4 + x + .4$ - the values of x are the roots of the equation
- Applying the Intermediate Value Theorem:
  - If we can find a value of $x$ that makes the equation equal a negative number, and some other value of $x$ that makes the equation equal a positive number, than it must be the case that there is at least one value of $x$ which makes the equation equal to 0
    - 0 is in between (an intermediate value) between any negative and any positive number

#### Example:

- This equation has real-valued Roots and we can set $x$ to a value to get 0
  $$f(x) x^4 + x + .4$$
- This equation has **no real-valued Roots** or solutions for $x$ to produce 0
  $$f(x) = x^4 + x + .5$$
