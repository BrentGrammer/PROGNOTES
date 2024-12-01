# Vectors

- [Python Notebook](./vectors.ipynb)

- Ordered set of numbers

  $$
  \begin{pmatrix}
  x_1 \\
  x_2 \\
  \vdots \\
  x_n
  \end{pmatrix}
  $$

- Each number in a vector is called an **Element**
- Elements in a vector can be fractions, integers, irrational, complex, etc.
  - **vectors can also contain functions as the elements**
- **Dimensionality**: Number of elements in a vector
  - $\begin{bmatrix}{1,2}\end{bmatrix}$ is a 2-D vector (**{1,2,3}** would be a 3-D vector, etc.)

### Two types of Vectors

- **Column**: $\begin{bmatrix}x_1\\x_2\end{bmatrix}$
- **Row**: $\begin{bmatrix}x_1x_2\end{bmatrix}$

### Notation

- $\overrightarrow{\text{v}}$ and some other similar variations
- common to use a bold lowercase **v**
  - Matrices are notated with CAPITOL letters (**V**)

### Geometric Interpretation of a Vector

- A straight line with some length and some **direction** specified by the vector coordinates
- The length and direction from the START point to the END point (the coordinates) is what defines a geometric vector.
  - It does not matter specifically where the vector starts (multiple vectors of [1,2] can start in any different place and are all described by [1,2])
  - They are "robust to translation or rigid body motion"
  - \*Vectors starting at the origin (coords `0,0`) are convenient to work with
    - **"STANDARD POSITION"**: when vectors start at the origin
- **TAIL**: the starting point of the vector
- **HEAD**: the end point of the vector (drawn with an arrow at the end of the line)
- **A vector is not the same thing as a coordinate**
  - The HEAD represents the end location of the vector, not the x-y coordinates
    - i.e. $\begin{bmatrix}{1,2}\end{bmatrix}$ is not x = 1 and y = 2, it is **one step over from the TAIL and 2 steps up.**
    - Note: when the vector is in Standard Position (0,0 origin for the tail), then the vector elements do cooincide with x and y coordinates.
- NOTE: geometric vectors are useful in 2 and 3 dimensions, but beyond that you usually have to switch back to algebraic vectors.

# Adding and Subtracting Vectors

## Adding Vectors

- Simply add the elements (per row or column) of one vector to the other
- **All vectors must be the same dimensionality** (same number of elements in each)
  $$\begin{bmatrix}1 \\0 \\4 \\3\end{bmatrix} + \begin{bmatrix}2 \\-3 \\-2 \\1\end{bmatrix} = \begin{bmatrix}3 \\-3 \\2 \\4\end{bmatrix}$$

### Geometric Interpretation

- Put the TAIL of one vector at the HEAD of the other vector
  - See [video](https://www.udemy.com/course/linear-algebra-theory-and-implementation/learn/lecture/10500380) at timestamp 1:49
  - The Vector Sum is the straight line vector from the TAIL of the first vector to the HEAD of the last vector
    - see [video explanation](https://www.udemy.com/course/linear-algebra-theory-and-implementation/learn/lecture/10500380) at timestamp 7:09

## Subtracting Vectors

### Two ways to think about subtracting vectors

#### 1.

- You can think of adding two vectors, but multiply all the elements in the second vector by -1.
- Has the effect of flipping/rotating the vector the other way
  $$\begin{bmatrix}1 \\2\end{bmatrix} + \begin{bmatrix}-2 \\-1\end{bmatrix} = \begin{bmatrix}-1 \\1\end{bmatrix}$$

#### 2.

- Put both vectors in standard position (geometric interpretation, i.e.2d or 3d)
- The subtracted vector's head becomes the new TAIL and the positive vector's HEAD becomes the new HEAD
  $$\begin{bmatrix}1 \\2\end{bmatrix} - \begin{bmatrix}2 \\1\end{bmatrix} = \begin{bmatrix}-1 \\1\end{bmatrix}$$

# Multiplying Vectors (Scalar Multiplication)

- **Changes the length, but preserves the direction of a vector**
  - Foundation and fundamental concept used in eigen value decomposition

### Scalar

- Single numbers
- notated with lowercase non-bold greek letters (alpha, beta, lambda): $\alpha {\space} \beta {\space} \lambda$

### Algebraic Interpretation

- Multiply each element of the vector by the scalar:
  $$7{\begin{bmatrix}-1 \\0 \\1\end{bmatrix}} = {\begin{bmatrix}-7 \\0 \\7\end{bmatrix}} $$

### Geometric Interpretation

- Stretch or Shrink the vector by the amount specified by the Scalar
  - Does NOT change the direction of the vector
  - the Scalar "scales" the vector
- $\lambda>1$: If the Scalar is greater than 1, it will scale the vector larger/longer
- $\lambda \epsilon(0,1)$: If between 0 and 1, the resulting vector points in the same direction and will be smaller/shorter than the original.
  - The epsilon $\epsilon$ means that lambda (the Scalar) is a member of or belongs to the set between 0 and 1
- $\lambda<0>$: When scalar is a negative number, the result is a "spun around" vector pointing the other way.
  - Note, that the vector is not technically pointing in a "different" direction (it is still on the infinite line in the one dimensional subspace that extends infinitely)
- NOTE: all vectors that are produced from a scaled vector all lie in the same **subspace**

# The Dot Product

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

### Commutative Property