# Continuous and Discontinuous Functions

- [python notebook](./discontinuousfunctions.ipynb)
- [Limits Notebook - see cells on limits with discontinuities](./Limits.md)

- Continuous: You can trace the plot of a function without lifting your finger off the plot
- Discontinuous: There is a break in the plot of a function
  - Note, subdomains (part or piece of the function outputs) can be continuous, but the whole is broken up
- See [visualization](https://www.udemy.com/course/pycalc1_x/learn/lecture/33947222) at timestamp 1:32 for examples of continuous and discontinuous function plots

### Continuous Function

- A function is continuous if the following 3 conditions are met, otherwise the function is discontinuous at point $a$:

1. $f(a)$ is defined
2. $\lim_{x \to a} f(x)$ exists.
   - (_This also means that both sides of the limit exist and they are equal to each other_).
   - Note that the limit for infinite discontinuities is defined as infinity - but not all of the other rules hold.
3. $\lim_{x \to a} f(x) = f(a)$ - the Limit equals the actual value of the function at point $a$
   - (Note: the limit is not technically the same thing as the function value - it is what happens as a function approaches that value without actually being equal to $a$. This statement is not redundant, but holds with continuous functions)
   - You can also combine this with the first rule that $f(a)$ is defined, since that is implicit in this rule.

### Continuity is technically about points

- Technically and formally continuity refers to points, though we can casually say a function is continuous/discontinuous
- If a function has a removeable discontinuity (a missing point that is undefined), technically we say that the function is continuous at all points except where the one is missing.

## Types of Discontinuities

### Jump discontinuity

- The function suddenly jumps from one value to another values without going through any vals in between

#### Definition/Characteristics of Jump Discontinuity:

- The two one-sided limits exist, but are not equal to each other.

### Infinite discontinuity

- The function blows up to infinity or minus infinity at a certain point (and can come up from negative infinity)
  - The Trig function Tangent is an example of this kind of discontinuity since it blows up to infinity
- The discontinuities (empty spaces between the continuous domains that go to or from infinity off the plot) are also called **Singularities**

#### Definition/Characteristic:

- Both one sided limits exist, but are both infinity

### Removable discontinuity

- The function is almost completely continuous, but there is one point where it breaks into a discontinuity and continues as if continuous again
  - On a plot typically a large empty circle is drawn on the point of discontinuity (often it is just an infinitesimal point in the function) to show that the function is missing a value at one individual point
  - Example function with a removable discontinuity when x = 2, the output is 0/0 (does not exist):
    $$f(x) = {{x^2 - 2x} \over {x^2 - 4}}$$

#### Definition/Characteristic:

- Both one-sided Limits are defined and equal to each other, but the Limit does not equal the function value at that point.

### Oscillating Discontinuity

- The function oscillates continually to infinity or infinitely close to some specific number
  Example:
  $$f(x) = \sin({1\over{x-1}})$$
  $$D : -1 \leq x \leq 2$$

## Definition of Continuity

1. $f(a)$ is defined
1. $\displaystyle\lim_{x \to a} f(x)$ exists (output when the limit of f(x) as you approach a exists)
1. $\displaystyle\lim_{x \to a} f(x) = f(a)$
