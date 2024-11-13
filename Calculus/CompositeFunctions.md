# Composite Functions

- [Python Notebook](./inversefunctions.ipynb)

- Composing functions by using the output of one as the input to another
  - Since functions map a variable onto another variable ($f(x) = y$ maps $x$ onto $y$), we can also push $y$ into another function
    $$x \rightarrow f(x) \rightarrow y \rightarrow g(y) \rightarrow z$$
- A composite function combines $f(x)$ and $g(y)$ into a single statement
  $$g(f(x))$$
  - $f(x)$ is set as the input into function $g$
  - The innermost function is applied first ($f(x)$ is applied first, and then $g(f(x))$ is applied)
    - Note $g$ is not applied to $x$, but to $y$ which is a transformation of $x$

### Example of a Composite function

$$f(x) = 2x^2 - 4$$
$$g(x) =  7x + 3$$
$f(g(x)) = 2(7x + 3)^2 - 4$

- $x$ in the first function $f(x)$ is set to the $g(x)$ function, or $7x + 3$ function

  <br>$= 2(7x +3)(7x + 3) - 4$
  <br>$= 2 (49x^2 + 21x + 21x + 9) - 4$
  <br>$= 98x^2 + 84x + 14$

## Commutivity

- Commutivity is being able to reverse the order of the operation and result is the same: $3 \times 4 = 4 \times 3$
  - applies to addition and multiplication, but not subtraction, etc.

**IMPORTANT**

- $g(f(x))$ and $f(g(x))$ are DIFFERENT functions with different outputs even if $x$ is the same value. You cannot apply commutivity in general to most Composite Functions.
  - Note: some specific pairs of composite functions can be commutative

### Notation

$$g(f(x)) \leftrightarrow (g \circ f)(x)$$

### Thinking in Domains

- Good idea is to think of the domains (range of inputs) for each individual function in a composite function vs. the domain of the whole composite function, and whether the restrictions of a domain of one of the sub functions affects the overall domain
