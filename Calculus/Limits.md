# Limits

- The behavior or value/output of a function as it gets closer and closer to, or approaches, a point with out actually reaching that given value
  - Ex: As $x$ approaches 2, the function output $y$ approaches 7 (The limit of some function $f(x)$ as $x$ approaches 2 is 7)
  - see [Zeno's paradox](./zenosparadox.ipynb)
- The limit has to do with the infinitessimally small point closest to a given value or point
  - _We are not interested in exactly what happens when we get to a given point in a function_, but what happens as we get closer and closer to that point

### Easy Limit

- The Limit of a function as it approaches point $a$ is actually the value of the function at point $a$
  - **NOTE: Do not assume this! It is just a shortcut that can work to quickly compute a Limit for easy limits**
- Easy Limits and Continuity are closely related: The function will be continuous at point $a$ where $a$ is an Easy Limit
  - Discontinuities make limits less easy to surmise

## Notation

$$\lim_{x \to a^-} f(x) = L$$

$$\lim_{x \to a^+} f(x) = L$$

- "The limit as `x` goes to `a` of the function `f(x)` is `L`"
- The plus and minus sign after `a` indicate which direction the limit is being computed for (left or right side on the slope) - "One Sided Limits"
  - `+` means approaching from relatively positive values (on the right of the number line)
  - `-` as you approach from relative negative values to the left of `a`
- Note that with limits we are not interested in exactly what happens when `x` = `a`, we're interested in what happens as `x` gets closer and closer to `a`
  - The function `f(x)` goes to `L` as `x` gets closer to `a`

### Example

$$\lim_{x \to 2}({{x^2 + 3x - 10} \over {x-2}}) = 7$$

# Easy Limits

- [video Lecture](https://www.udemy.com/course/pycalc1_x/learn/lecture/33947296)

## Solving Easy Limits

### A Simple Solution

- First thing to try is simply plug in $x$, the limit x value, to get the Limit of the Function:

$$\lim_{x \to 2}(x^2 + 3x - 10) = 0$$

- Plugging in the value $2$ (where the limit goes to) gives us 0 at $x = 2$, so the limit of the function as $x$ approaches 2 is 0 (the output approaches 0 as $x$ moves towards 2)

### Dealing with Discontinuities

#### Pay attention to whether a tiny change in $x$ results in a similar tiny change in the function output (i.e. if there are discontinuities, jumps, etc. at the limit - i.e. point $x = 2$)

- For example in this function, plugging in $x = 2$ gives a removable discontinuity since we are then dividing by 0 and output is undefined at that small specific point:
  $$\lim_{x \to 2}{{x^2+3x-10} \over {x-2}}$$
  - In this case we could try some algrebraic tricks to modify or cancel the denominator so that it does not equal 0 when $x=2$ (i.e. here, we can factor the numerator, and cancel out $x-2$):
    $$\lim_{x \to 2}{{(x+5)(x-2)} \over {x-2}} = \lim_{x \to 2}(x+5) = 7$$
  - This simplification leads us to the solution: As $x$ approaches 2 (the limit), the Function output/value approaches 7
    - Note that the function is still undefined when $x=2$, this is just a shortcut way to compute an easy limit

# One Sided Limits

### Function with Two Limits

- We have two One Sided Limits to the following function depending on whether we approach the target value from the left or the right:
  $$\lim_{x \to 2}{{{|x-2|}} \over {x-2}}$$
- In this example, both are valid Limits, but the left and right limits are not equal to each other
  $$\lim_{x \to 2^-}{{{|x-2|}} \over {x-2}} = -1$$
  $$\lim_{x \to 2^+}{{{|x-2|}} \over {x-2}} = +1$$
- Use the `-` and `+` superscript with the limit X value to signify whether the One Sided Limit is the left or right
  - (The two sided Limit just doesn't exist and is undefined in this case, and the function itself is undefined at $x=2$ since we just get $0 \over 0$)

### **NOTE: Having unequal One Sided Limits does NOT necessarily mean that the function is undefined at that point and it's Two Sided Limit may not exist**

- Example: The "Heaviside Function", which has a Jump Discontinuity and unequal One Sided Limits, while having no 2 sided Limit, but is still defined for all $x$ values:
  $$
      H(x) = \begin{cases}
        1 , & x > 0 \\
        0 , & x \leq 0
      \end{cases}
  $$
- This function is defined everywhere, including at the Jump Discontinuity when $x=0$
- The two One Sided Limits are unequal as well:
  $$\lim_{x \to 0^-}H(x) = 0$$
  $$\lim_{x \to 0^+}H(x) = +1$$
- The Limit (two-sided) of this function Does Not Exist (Notated as `d.n.e.`): $\lim_{x \to 0}H(x) = d.n.e.$

### Generalization of One Sided Limits

- **If a function has two different One-Sided Limits, then the function is DISCONTINUOUS at that point**
- The equality of two One-Sided Limits is the _definition_ of CONTINUITY
  $$\lim_{x \to a^-} = \lim_{x \to a^+} \longrightarrow \text{The Limit exists}$$
  $$\lim_{x \to a^-} \neq \lim_{x \to a^+} \longrightarrow \text{The Limit does not exist}$$

### One Sided Limits to Infinity

- Generally you see functions blow up to Infinity when $x$ is in the denominator
  - As $x$ gets closer and closer to 0, the function output gets higher and higher
  - In this case there are one sided Limits on both sides AND a two-sided standard Limit

$$\lim_{x \to a^-}f(x) = \infty$$
$$\lim_{x \to a^+}f(x) = \infty$$
$$\lim_{x \to a}f(x) = \infty$$
