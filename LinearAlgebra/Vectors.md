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

## Computing the Length (Magnitude/Norm) of a Vector

- The length can be referred to as the "magnitude" or the "norm"
- Take the square root of the dot product of the vector with itself
  $$||v|| = \sqrt{\textbf{v}^T\textbf{v}}$$
- This formula works because of the pythagorean theorem.
  - The length of a vector in standard position could be thought of as the hypotenuse
  - The first element in vector $\begin{bmatrix}2,3\end{bmatrix}$ for example, is 2 which is the length of the adjacent side of a right triangle when projected to the x-axis, and 3 which is the length of the opposite side of a right triangle (vertical height). so $||v||^2 = (v_1)^2 + (v_2)^2$, i.e. $c^2 = a^2 + b^2 = 2^2 + 3^2 = 13$, and therefore the square root of 13 is vector length $||v||$
  - The algebraic application (vs. the geometrical in 2d or 3d) becomes useful in higher dimensions

### The Length/Magnitude of the Dot Product of Two Vectors

- You do not take the square root when computing the magnitude of a dot product/scalar, you just take the absolute value (to represent length on a 1D number line to the origin):
  $$|v^Tv| = ||v^Tv||$$
- The dot product between two (different) vectors is not Euclidean length, so you don't need to take its square root. If you wanted to compute the distance between two points, then you would need the square root.

- You can also think about the geometric interpretation of the dot product -- the magnitude of one vector times the magnitude of the other vector times the cosine of the angle between them. That's also not a length. Or think about two vectors that are really long, like as long as the observable universe. But they meet at a right angle, so the dot product between them is 0.

- Now, when the two vectors are the same, then the angle is 0 and cosine of that is 1. So then the dot product of a vector with itself ends of being the same as the length squared. But the dot product on its own is not a measure of length, because it's also dependent on the angle.

## Scalar

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

# Hadamard (Element-wise) Multiplication of Vectors

- 2 vectors must be same size/dimensionality

$$\begin{pmatrix} 1 \\ 0 \\ 2 \\ 5 \\ -2 \end{pmatrix} \odot \begin{pmatrix} 2 \\ 8 \\ -6 \\ 1 \\ 0 \end{pmatrix} = \begin{pmatrix} 2 \\ 0 \\ -12 \\ 5 \\ 0 \end{pmatrix}$$

# Vector Multiplication

- See [Notebook](./vectormultiplication.ipynb)

## The Dot Product

- See [NOTES](./DotProduct.md)

## The Inner Product

- See [Notes](./OuterProduct.md)
- Alternative to the Dot Product

## Cross Product

- See [Notes](./CrossProduct.md)

# The Unit Vector

## Definition

- A Vector with a length of 1
  - The "Unit Number" is the number 1
- _You can compute the Unit Vector for another vector that will be the same orientation/angle/direction, but its length will be transformed to 1 from the original length_
- Used in Statistics (Correlation Coefficient b/w two vars - Pearson Correlation Coefficient), Machine Learning (Cosine Similarity), useful for Basis Vectors (they only change direction/orientation, not length)

### Algebraic Definition:

- Some vector that is a scaled multiplication of $v$ - $\mu \textbf{v}$ - such that (s.t.) the magnitude (length - $||$) of $\mu \textbf{v}$ is equal to 1
  $$\mu \textbf{v} \space \text{s.t.} \space ||\mu \textbf{v}|| = 1$$

### Principles

- All vectors have some length and some orientation
- All vectors with the same orientation (the same angle) are related to each other by some scalar multiplication
  - This allows you to create a Unit Vector in the same direction as some other vector

### Finding $\mu$ - the scalar to get a Unit Vector

- **To get the Unit Number (1) by multiplying by any number, you can multiply the number by its recipricol to get 1**:
  $$\mu 3 = 1 \rightarrow \mu = 1/3$$
- To find the scalar necessary to scale a vector to get a unit vector, take the reciprocol of the magnitude (length) of that vector:
  $$\mu = {1 \over{||\textbf{v}||}}$$

#### EXCEPTION: The Zero Vector

- A vector containing all zeros does NOT have a corresponding Unit Vector
  - Geometrically this vector has no length and is just a point, so it's not possible to define some other vector in the same direction of the Zero Vector
