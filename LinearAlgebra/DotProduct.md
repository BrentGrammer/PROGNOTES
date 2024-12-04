# The Dot Product

- See [Python Notebook](./dotproduct.ipynb)

- A single number that provides information about the relationship between two vectors
  - a.k.a. "The Scalar Product"

### Notation

- Numerous ways of notating the dot product:
  - greek letter (alpha),
  - a times b
  - wide angle brackets
  - aTb for "transposed" (the first vector transposed times the second vector. This is the most common notation in linear algebra),
  - the algebraic definition: element-wise multiplication and the sum of all the corresponding elements of the two vectors
    $$\alpha = a \cdot b = \left\langle a,b \right\rangle = a^Tb \space\text{(most common in lin. alg.)} = \sum^n_{i=1}a_ib_i$$

### Computing the Dot Product

- Both vectors must be the same size/dimensionality
  - Otherwise the dot product is undefined
- Do elementwise multiplication, and sum all the products together for the final result:

$$\begin{bmatrix}1 \\0 \\2 \\5 \\-2\end{bmatrix} \begin{bmatrix}2 \\8 \\-6 \\1 \\0\end{bmatrix}$$
$$\textbf{v}^T\textbf{w} = 1 * 2 + 0 * 8 + 2 * (-6) + 5 * 1 + (-2) * 0 = -5$$

## Properties of the Dot Product

### The Distributive property (The dot product IS)

- Distribute the $a$ into each term:
  Ex: $a(b+c) = ab + ac$
- The vector dot product is distributive:
  - $\textbf{a}^T(\textbf{b}+\textbf{c}) = \textbf{a}^T\textbf{b} + \textbf{a}^T\textbf{c}$

### The Associative Property (The dot product is NOT)

- In most linear algebra, you can change parentheses anywhere with multiplication: $a(b\cdot c) = (a \cdot b)c$
- The Dot Product is NOT associative
  - $\textbf{a}^T(\textbf{b}^T\textbf{c}) \neq (\textbf{a}^T\textbf{b})^T\textbf{c}$
  - One side can produce a column while the other produces a row, or vector pairs could be different dimensions, etc.
  - Note: there are rare special cases where this does not hold and it is associative
    - one vector is the zeros vector
    - case 2, all vectors equal to each other: $a = b = c$
  - Also Note: matrix multiplication, otoh, is associative

### Commutative Property for the Dot Product

- Commutative Property: $a^Tb = b^Ta$ (i.e. you can swap the order of the vectors and the result remains the same, the dot product between $a$ and $b$ is the same as between $b$ and $a$)
- The Dot Product IS Commutative because it is based on scalar multiplication (which is commutative)
  $$\begin{bmatrix}2, 4\end{bmatrix} * \begin{bmatrix}3, 5\end{bmatrix} = 2*4 + 3*5 = 4*2 + 5*3$$

## Computing the Length of a Vector

- The length can be referred to as the "magnitude" or the "norm"
- Take the square root of the dot product of the vector with itself
  $$||v|| = \sqrt{\textbf{v}^T\textbf{v}}$$
- This formula works because of the pythagorean theorem.
  - The length of a vector in standard position could be thought of as the hypotenuse
  - The first element in vector $\begin{bmatrix}2,3\end{bmatrix}$ for example, is 2 which is the length of the adjacent side of a right triangle when projected to the x-axis, and 3 which is the length of the opposite side of a right triangle (vertical height). so $||v||^2 = (v_1)^2 + (v_2)^2$, i.e. $c^2 = a^2 + b^2 = 2^2 + 3^2 = 13$, and therefore the square root of 13 is vector length $||v||$
  - The algebraic application (vs. the geometrical in 2d or 3d) becomes useful in higher dimensions
