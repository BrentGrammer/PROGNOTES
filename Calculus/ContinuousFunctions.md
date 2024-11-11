# Continuous and Discontinuous Functions

- Continuous: You can trace the plot of a function without lifting your finger off the plot
- Discontinuous: There is a break in the plot of a function
  - Note, subdomains (part or piece of the function outputs) can be continuous, but the whole is broken up
- See [visualization](https://www.udemy.com/course/pycalc1_x/learn/lecture/33947222) at timestamp 1:32 for examples of continuous and discontinuous function plots

## Types of Discontinuities

### Jump discontinuity

- The function suddenly jumps from one value to another values without going through any vals in between

### Infinite discontinuity

- The function blows up to infinity or minus infinity at a certain point (and can come up from negative infinity)
  - The Trig function Tangent is an example of this kind of discontinuity since it blows up to infinity

### Removable discontinuity

- The function is almost completely continuous, but there is one point where it breaks into a discontinuity and continues as if continuous again
  - On a plot typically a large empty circle is drawn on the point of discontinuity (often it is just an infinitesimal point in the function) to show that the function is missing a value at one individual point
  - Example function with a removable discontinuity when x = 2, the output is 0/0 (does not exist):
    $$f(x) = {{x^2 - 2x} \over {x^2 - 4}}$$

## Definition of Continuity

1. $f(a)$ is defined
1. $\displaystyle\lim_{x \to a} f(x)$ exists (limit of f(x) as you approach a exists)
1. $\displaystyle\lim_{x \to a} f(x) = f(a)$
