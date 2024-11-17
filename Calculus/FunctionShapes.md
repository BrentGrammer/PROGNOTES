# Function Shapes

- See [video](https://www.udemy.com/course/pycalc1_x/learn/lecture/33947256) at timestamp 2:44 for overview of some common function shapes
- [Python Notebook](./functionshapes.ipynb)

## Sketching Function Shapes

### Being familiar with function shapes

[video](https://www.udemy.com/course/pycalc1_x/learn/lecture/33947256) at timestamp 2:44 for overview of some common function shapes

- Linear functions like $y=x$ - straight line
- Polynomial functions with even orders: $y = x^2$ - U shaped line
  - **The long run behavior of a polynomial is driven by the highest power - look at the term with the highest power in the equation for a shortcut to interpreting the rough shape.**
- Polynomials with odd orders: $y = x^3$ - S shaped line
- Trig functions (Sine and Cosine) - Wave
- Tangent (Trig) function - Blows up to +Infinity and comes up from -Infinity
- $y = 1/x$ : two curvy L shaped lines diagonally across from one another with discontinuity at 0
- $y = 1/x^3$ : two more square edged L-shaped lines diagonally across from each other with discontinuity at 0
- $y = 1/x^2$ : Even exponents in the denominator will always be positive and blow up to positive Infinity on both sides of the x-axis = 0 tick.
- Logarithmic functions like $y = \ln(x)$ and $y = \sqrt{x}$ have similar properties of the shape (steeper curve and the beginning that gets less steep towards the end)
  - Key difference from $\sqrt{x}$ is that the log of a number less than 1 is negative and goes down to -Infinity for $ln$ shapes.
- Natural Exponent function $e^x$ : not steep and gradual incline at the beginning and gets very steep as trajectory continues
- [More Shapes](https://www.udemy.com/course/pycalc1_x/learn/lecture/33947292) at timestamp 3:48
  - $f(x) = e^{-x}$ : looks similar to $1/x$, but it does not blow up to infinity as $x$ approaches 0, instead it blows up to higher output as $x$ goes to/approaches negative infinity, **the negative x in the exponent makes the number exponentially higher to the negative side**
  -

### Understand the Domain of the Function

- Think about where the function will be undefined for real valued numbers

### Solve the function for a couple of easy points

- This helps you get a couple of points to draw on a graph for a quick sketch of the function shape
- e.g. $x = \{-1,0,1\}$
  - For example with a function like $f(x) = {{x-4} \over {x^2-1}}$, we know if $x = 4$, the output is always 0 since if the numerator is 0, no matter what everything else is, the answer will be 0

### Consider what happens when input X gets really large

- Figure out what happens when $x$ gets very large (infinity) or very small (minus infinity)
- In $f(x) = {{x-4} \over {x^2-1}}$ as $x$ gets very large, the output tapers down towards 0 as the denominator increases exponentially vs. the linearly increasing numerator

### Look for Discontinuities (understand the Limits of x)

- In $f(x) = {{x-4} \over {x^2-1}}$ if $x = -1$ or $x = 1$, those are two discontinuities that will make the denominator 0 and the output undefined.
- **The important thing to note is not where the discontinuity actually occurs, but what happens when $x$ is very near that point where the discontinuity occurs**
  - See [video example](https://www.udemy.com/course/pycalc1_x/learn/lecture/33947256) at timestamp 9:58
