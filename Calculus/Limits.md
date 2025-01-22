# Limits

- [Python Notebook on Limits](./limits.ipynb)

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

## Properties of Limits

4 Main Properties:

### Limits are Factorable:

- $f$ is a function $f(x)$ and $c$ is some constant
- The Limit as some variable approaches some value, where some $c$ times some function $f$ is the same thing as $c$ times the Limit of that function.
  - **You can factor out the Constant from inside of a function to outside of a function**
  - Important for understanding why some deritaves of some functions are the way they are.
    $$\lim_{x \to n}(cf) = c\lim_{x \to n}$$

### Limits are Additive

- The Limit of the Sum of two functions, $f$ and $g$, is the same as the Limit of each function computed separately, and then added together.
  - The Limit values (what $x$ goes to) must be the same for all the Limits in the equation above.
    $$\lim_{x \to n}(f+g) = \lim_{x \to n} f + \lim_{x \to n} g$$

### Limits are Multiplicative

- The Limit of $f(x)$ times $g(x)$ is the same thing as the Limit of $f(x)$ times the Limit of $g(x)$
  $$\lim_{x \to n}(f \times g) = (\lim_{x \to n} f) \times (\lim_{x \to n} g)$$

- Works for exponents as well:
  $$\lim_{x \to n}(f^3) = (\lim_{x \to n} f) \times (\lim_{x \to n} f) \times (\lim_{x \to n} f)$$

### The Divisive Property of Limits

- The Limit of $f(x)$ divided by $g(x)$ is the same as the Limit of $f(x)$ divided by, the separate term which is, the Limit of $g(x)$
  $$\lim_{x \to n}(f/g) = (\lim_{x \to n}f) / (\lim_{x \to n}g)$$
- **NOTE**: This property only holds if the Limit exists.
  - If any limit is undefined, in this case the denominator is 0, the results will not be equal as in $\lim_{x \to 0}f(g) / \lim_{x \to 0}(x^3 + x^2 + x)$

# Important Limits of Trig Functions

- see [Python Notebook](./triglimits.ipynb)

These functions are important for differentiating sin and cosine

- The limit of this function as angle phi approaches 0 is 0 (the function output):
  $$\lim_{\phi \rightarrow 0}\left[{{\cos(\phi)-1} \over \phi}\right] = 0$$
- The limit of this function as angle phi approaches 0 is 1 (the function output):
  - See a visual geometric proof of this in [video](https://www.udemy.com/course/pycalc1_x/learn/lecture/33947318) at timestamp 4:52
  - The $\sin(\phi)$ is the vertical edge of the triangle (length of the line corresponding to the y-axis intercept), and as angle phi gets closer to 0, the ratio of the arc of the unit circle for the triangle goes to 1.
  - It represents a ratio of a straight line (vertical edge) to the arc on the unit circle, and as the angle gets smaller and smaller to 0, the line and arc converge to become the same length
    $$\lim_{\phi \rightarrow 0}\left[{{\sin(\phi)} \over \phi}\right] = 1$$
    (Note: in either of these cases if phi = 0, there is a discontinuity as you can't divide by 0)

## Squeeze Theorem (a.k.a. sandwich/pinch theorem)

See [video](https://www.udemy.com/course/pycalc1_x/learn/lecture/33947322) at timestamp 3:30

- A way to find the limit at a point in a function where it's very difficult or otherwise impossible to calculate the limit

  - i.e. there is a discontinuity at the point of the limit, etc.
  - Also useful if there are situations where it's very hard to compute the derivative of a function at a point.

- Define two other functions $g(x), h(x)$ around the point of the original function $f(x)$ that are easier to compute the limit for, take their limits and conclude that the limit of $f(x)$ is in between the limits of $g(x)$ and $h(x)$
- The squeeze or sandwich is taking points in the other two functions that are near or just below and above the point in the original function:
  - the output of $g(a)$ is smaller or equal to the output of $f(a)$ which is smaller or equal to the output of $h(a)$
    $$g(a) \leq f(a) \leq h(a)$$
  - The limit of $f(x)$ as $x$ approaches point $a$ must be in between the limit of $g(x)$ and $h(x)$ as both of them approach point $a$
    $$\lim_{x \rightarrow a}g(x) \leq \lim_{x \rightarrow a}f(x) \leq \lim_{x \rightarrow a}h(x)$$
  - If the limits of $g(x)$ and $h(x)$ at point $a$ are the same, then the limit of $f(x)$ for $a$ must also be the same
    $$L \leq \lim_{x \rightarrow a}f(x) \leq L$$

### Choosing the other functions to squeeze the original with:

- \*\*You need to make sure that the two outer functions at point $a$ pinch the point and squeeze closely around the point of the original function for the squeeze theorem to be useful. Otherwise the range is too large as to what the limit of the original function could be.
  - It can be useful, however to know the rough boundaries of where the limit of your original function could fall between, even if that range is wide.
- There's trial-and-error and some intuition involved, but you want to pick functions that are easy to work with and easy to manipulate (that is, have a particular value at a particular point). Quadratic functions like y=x^2 are popular for this reason. You can stretch and shift these functions as you need, e.g., y=(x-3)^2

### Example using the Squeeze theorem

- The limit for this function as x approaches 2 cannot be computed because there is a discontinuity at x=2 (the output is division by 0 / 0 and does not exist)
  $$f(x) = {{x^2 - 2x} \over {x^2 - 4}}$$
- Make two other functions that are easier to calculate the limit of as x approaches 2:
  $$g(x) = .5 + (x-2)^2$$
  $$h(x) = .5 - (x-2)^2$$
  $$.5 \leq \lim_{x \to 2}f(x) \leq .5$$

### Example squeeze theorem with simple Trig function

- Finding the limit of $f(\theta)$ as $\theta$ approaches $0$
  $$f(\theta) = \theta \cos{(\theta)}$$
  $$\lim_{\theta \to 0} = ?$$
- Use the boundaries of $\cos$ ($-1$ and $1$) and multiply through the differences against the original equation
- $\cos$ is bound from -1 to 1, so we can assume the boundaries (if we multiply the variable $\theta$ by -1 or 1 at either end):
  $$-\theta \leq \theta \cos(\theta) \leq \theta$$
- You can use two functions to squeeze with:
  $$g(\theta) = -\theta$$
  $$h(\theta) = \theta$$
- plugin limits as $\theta$ approaches $0$ for $h(\theta)$ and $g(\theta)$ which are $0$, so:
  $$0 \leq \lim_{\theta \to 0}f(\theta) \leq 0$$

### Example Trig Function Limits using the Squeeze Theorem

- The squeeze theorem can be applied to many problems of figuring out the limit of trig functions
- This trig function has a discontinuity at $\theta = 0$
  $$\lim_{\theta \to 0} f(\theta) = \theta^2\sin \left({1 \over \theta}\right)$$
- Again, we can use the fact that $\sin$ is bounded by -1 and 1 to give us $-\theta^2 \leq \theta^2\sin\left({1 \over \theta}\right) \leq \theta^2$
- So we find the limits of functions $-\theta^2$ and $\theta^2$ which is $0$ via the plugin method:
  $$-0 \leq 0 \leq 0$$

### Example 2

- In this example, the numerator is always changing as $\theta$ goes to infinity (which gives us an oscillating discontinuity)
  $$\lim_{\theta \to \infty}\left({\sin\theta \over \theta}\right)$$
- We can isolate $\sin\theta$ and based on the bounds of $\sin$ again and make the numerator constant by dividing the bounds by $\theta$ as well as $\sin\theta$
  $${-1 \over \theta} \leq {\sin\theta \over \theta} \leq {1 \over \theta}$$
- We take the limits as $\theta$ goes to $0$ of the outer functions squeezing our original function which gives us:
  $$-0 \leq 0 \leq 0$$

### Example 3

$$\lim_{\theta \to 0}\left[\tan(\theta) \over \theta\right]$$

- We can rewrite this to split the $\tan$ as a ratio and then swap the denominators:
  $${\tan(\theta) \over \theta} = {{\sin\theta / \cos\theta} \over \theta} = {\sin\theta \over \cos\theta} \times {1 \over \theta} = {\sin\theta \over \theta} \times {1 \over \cos\theta}$$
- Using the multiplicative property of limits, we now have:
  $$\lim_{\theta \to 0}\left[{\tan(\theta) \over \theta}\right] = \lim_{\theta \to 0}\left({\sin\theta \over \theta}\right) \times \lim_{\theta \to 0}\left({1 \over \cos\theta} \right)$$
- $\sin\theta$ divided by $\theta$ is 1 and the $\cos$ of $0$ is $1$, using the plugin method we get the solution:
  $$1 \times 1 = 1$$
