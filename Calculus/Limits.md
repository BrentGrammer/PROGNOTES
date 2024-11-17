# Limits

- The behavior or value of a function as it gets closer and closer to, or approaches, a point with out actually reaching that given value
  - see [Zeno's paradox](./zenosparadox.ipynb)
- The limit has to do with the infinitessimally small point closest to a given value or point
  - *We are not interested in exactly what happens when we get to a given point in a function*, but what happens as we get closer and closer to that point

### Easy Limit

- The Limit of a function as it approaches point $a$ is actually the value of the function at point $a$
- Easy Limits and Continuity are closely related: The function will be continuous at point $a$ where $a$ is an Easy Limit
  - Discontinuities make limits less easy to surmise

## Notation

$$\lim_{x \to a^-} f(x) = L$$

$$\lim_{x \to a^+} f(x) = L$$

- The limit as `x` goes to `a` of the function `f(x)` is `L`
- The plus and minus sign after `a` indicate which direction the limit is being computed for (left or right side on the slope)
  - `+` means approaching from relatively positive values (on the right of the number line)
  - `-` as you approach from relative negative values to the left of `a`
- Note that with limits we are not interested in exactly what happens when `x` = `a`, we're interested in what happens as `x` gets closer and closer to `a`
  - The function `f(x)` goes to `L` as `x` gets closer to `a`

### Example

$$\lim_{x \to 2}({{x^2 + 3x - 10} \over {x-2}}) = 7$$

# Easy Limits

- [video Lecture](https://www.udemy.com/course/pycalc1_x/learn/lecture/33947296)