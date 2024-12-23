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

# Notes on Dimension

- Dimension represents the number of elements in a vector
- Each dimension in a vector can represent a new "feature" or new piece of information about the Vector
- Each dimension represents a new geometric direction
- The axes on a geometric plane in linear algebra correspond to a dimension (element) in a Vector

  - i.e. instead of x and y axes, for a given vector $v$, we would have $v_1$ and $v_2$ axes for a 2-D Vector, for example

- NOTE: A 3-Dimensional Vector is still a line (i.e. 1-D subspace embedded in 3 Dimensions, for ex.), but it is 3-Dimensional because it has 3 elements.
  - It could be said that a 3-D vector corresponds to a line in a 3 Dimensional space

## Fields

- **Field**: A set of numbers, upon which a set of arithmetic (addition,subtraction,division,multiplication) can be used and is valid.

### Notation of Fields

- Indicated with a Hollow Letter symbol:
  $$\mathbb{R} - \text{Real Numbers}$$
  $$\mathbb{C} - \text{Complex Numbers}$$
  $$\mathbb{Z} - \text{Integers ("Counting Numbers" 1,2,3,4,5... Note: NOT a field!)}$$

#### Indicate Dimensionality in Superscript

- $N$ or $M$ in the superscript is a conventional place holder for the number of dimensions (i.e. two different sets of vectors with different dimensionalities, used in matrices often):
  $$\mathbb{R}^N, \mathbb{R}^M$$
- Example of dimensions specified:
  $$\mathbb{R}^2 \space \rightarrow \begin{bmatrix}3 -4\end{bmatrix}$$

#### Vectors can be Members of a Field

- Vectors can be members of ($\in$) a Field
- In this example, we can already tell by looking at this that the dot product of these two vectors $v$ and $w$ is not defined unless $N$ is equal to $M$, for example.F
  $$\textbf{v} \in \mathbb{R}^N$$
  $$\textbf{w} \in \mathbb{R}^M$$

# Subspace

- Encompass vectors based on **Linear Combinations** of Vectors: Scaling (multiplied by a Scalar) and addition if multiple vectors
- Subspaces are part of the **AMBIENT SPACE** (the total space of a plane or area they can fall in)

## Formal Definition of Subspace:

- A Vector subspace must
  - be closed under addition and scalar multiplication
    - "For any vectors, v and w that are both members of the subspace V, and for any Scalar lambda or alpha in the set of Real Numbers, lambda times v plus alpha times w is still a member of subspace V"
      $$\forall \textbf{v}, \textbf{w} \in V; \quad \forall \lambda,\alpha \in \mathbb{R}; \quad \lambda \textbf{v} + \alpha \textbf{w} \in V$$
      - Where $V$ is the subspace, $\forall$ means "for all", $v$ and $w$ are vectors and $\mathbb{R}$ is set of real numbers
      - i.e. **any way of combining the two vectors linearly results in another vector in the same subspace**
  - contain the zero vector (implied and given with the first condition above)
    - if you set the Scalar to be 0, then you get the zero vector (a vector of all zeros)

## Algebraic Interpretation of Subspace

- The set of all Vectors that can be created by taking linear combinations (multiplied by a scalar) of some vector $v$ or a set of Vectors, where the Scalar $\lambda$ is in a set of any Real Value number
  $$\lambda \textbf{v}, \lambda \in \mathbb{R}$$
- Any other Vector scaled as $\lambda \textbf{v}$ **is in the same subspace** as Vector $\textbf{v}$
  $$\textbf{v} = \begin{bmatrix}2 \\ 3\end{bmatrix} \rightarrow 2 \begin{bmatrix}2 \\ 3\end{bmatrix} = \begin{bmatrix}4 \\ 6\end{bmatrix} \text{(In the same subspace as $\textbf{v}$)}$$
  $$-3 \begin{bmatrix}4 \\ 6\end{bmatrix} = \begin{bmatrix}-12 \\ -18\end{bmatrix} \space \text{(Still in the same subspace as original vector (the **Basis Vector**) $\textbf{v} \space above!$)}$$
  - (If you took 3 and -2 together (-6) and scaled vector $\textbf{v}$ by that you can get to $\begin{bmatrix}-12 \\ -18\end{bmatrix}$, so it is still in the same subspace)
- A vector that cannot be multiplied by the same scalar $\lambda$ as another vector is NOT in the same subspace:
  $$\textbf{v} = \begin{bmatrix}2 \\ 3\end{bmatrix} \rightarrow \begin{bmatrix}2 \\ 4\end{bmatrix} \space \text{(Impossible for [2,4] to be in the same subspace as [2,3] with 1 as the Scalar)}$$

### Can have a Subspace of Multiple Vectors

- A Subspace can be defined by combining multiple vectors as well (all possible Linear Combinations of the two vectors)
  $$\lambda \textbf{v} + \beta \textbf{w}$$
- A Vector can be in the same subspace that can be defined by the Vectors $v$ and $w$
  $$6 \textbf{v} - 4 \textbf{w} = \begin{bmatrix}12 \\ 2\end{bmatrix}$$

## Geometric Interpretation of Subspace

### Single Vector

- If you take a vector and plot it on a graph, then think about all scaled versions of that vector, you'll find that they all lie on an infinitely long line (from $\lambda - \infty$ to $\lambda + \infty$)
  - One vector describes a line
  - All scaled versions of the vector represent a 1-Dimensional subspace

### Multiple Vectors

- The subspace of the combination of two vectors is a 2 Dimensional plane
  - The two vectors which are combined, even though individually they do not have to belong to the same subspace themselves, lie within the 2-D plane (for example on a 3-D plane) that goes infinitely long in all its 2-D directions, encompassing the subspace of their combination
- **ALL SUBSPACES INTERSECT AT THE ORIGIN**
  - All subspaces must necessarily include the origin
- **NOTE**: Having 2 vectors does not necessarily mean you get a plane for the subspace!
  - Vectors that are already in the same subspace lie along the same 1D subspace
    $$\lambda \begin{bmatrix}1 \\ 2 \\ 4\end{bmatrix} \quad \mu \begin{bmatrix}2 \\ 4 \\ 8\end{bmatrix}$$
    - Linear combinations of these two vectors do not result in a 2D subspace, but a 1D subspace, since they are both in the same subspace - the second vector is just a scaled version of the first
  - In order for the combination of 2 vectors to create a 2D subspace, the two vectors need to be independent of each other!

### Ambient Space

- The total area/plane space that all subspaces can fall into
- 0D Subspace - the point at the origin
  - There is only ONE 0D subspace
- 1D Subspaces - defined by a line
  - There are an infinite number of 1D subspaces embedded inside a 3D Ambient Space
- 2D Subspaces - planes
  - Infinite number of these that can be embedded within a 3D Ambient Space
- 3D Subspace - 3D area in the ambient space
  - There is only ONE 3D subspace that fits inside a 3D Ambient Space

### Subspaces with higher than 3D Ambient Space

- For $\mathbb{R}^5$ (5F Ambient Space)

  - 0D subspace = $[0,0,0,0,0]$
  - A 1D Subspace instance embedded in $\mathbb{R}^5$ Ambient Space: $[0,1,3,1,0]$ - This is a line in 5 Dimensional Space

    $$
    0D = \left\{
    \begin{bmatrix}
    0 \\ 0 \\ 0 \\ 0 \\ 0
    \end{bmatrix}
    \right\}

    1D = \left\{
    \begin{bmatrix}
    0 \\ 1 \\ 3 \\ 1 \\ 0
    \end{bmatrix}
    \right\}

    2D = \left\{
    \begin{bmatrix}
    0 \\ 1 \\ 3 \\ 1 \\ 0
    \end{bmatrix}
    \begin{bmatrix}
    9 \\ 4 \\ 2 \\ 3 \\ 1
    \end{bmatrix}
    \right\}
    $$

  - In this example of what looks like a 3D plane, it is actually just a 2D plane, because the last vector is just a scaled version of the 2nd vector - so the subspace is actually 2D!
    $$
    3D? (2D) = \left\{
    \begin{bmatrix}
    0 \\ 0 \\ 0 \\ 0 \\ 1
    \end{bmatrix}
    \begin{bmatrix}
    0 \\ 0 \\ 0 \\ 1 \\ 0
    \end{bmatrix}
    \begin{bmatrix}
    0 \\ 0 \\ 0 \\ 2 \\ 0
    \end{bmatrix}
    \right\}
    $$
  - Changing the 3rd vector does not make it a scaled version of another, so taking the combination of these 3 vectors actually creates a 3 Dimensional subspace embedded with $\mathbb{R}^5$:
    $$
    3D = \left\{
    \begin{bmatrix}
    0 \\ 0 \\ 0 \\ 0 \\ 1
    \end{bmatrix}
    \begin{bmatrix}
    0 \\ 0 \\ 0 \\ 1 \\ 0
    \end{bmatrix}
    \begin{bmatrix}
    0 \\ 0 \\ 1 \\ 0 \\ 0
    \end{bmatrix}
    \right\}
    $$
    - NOTE: In 5 Dimensional Ambient Space, this 3D subspace still does not fill up all of it as it would in a 3 Dimensional Ambient Space
    - This is called a **Hyperplane** - indicates some high dimensional space in some even higher ambient space

## Subset vs. Subspace

- A set of points that satisfies some conditions
  - Does not need to include the origin
  - Does not need to be closed (under multiplication/addition)
  - Can have boundaries
- Example: All points on the XY Plane such that x is greater than 0 and y is greater than 0
  - This is NOT a subspace, because:
    - the origin is not included (greater than 0)
    - Flipping the sign and multiplying a vector in this subset by the Scalar -1, puts it outside of the subset (-x and -y coordinates), therefore it is not a subspace because the first rule for a subspace is that any scalar of a vector must still remain in the subspace defined.
- A subset can be a subspace, but some subsets are NOT subspaces if they violate the rules of a subspace

# Spans

- Vectors can span a subspace
- The span of a set of vectors is all possible linear combinations of all the vectors in that set
- A common question in linear alg. is whether one vector is in the span of another or set of vectors

$$\text{span}(\{\textbf{v}_1,..., \space \textbf{v}_n\}) = \alpha_1 \textbf{v}_1 + ... + \alpha_n \textbf{v}_n, \space \alpha \in \mathbb{R}$$

- All possible lineaer weighted combinations of all the vectors in the set, where $\alpha$ is a member of all real numbers, spans some subspace
- The span can stretch to infinity since the Scalars can be arbitrarily large or small

### Spans

- A span of a set of vectors (in a set $S$, for example) is the entire space that can be reached by any linear combination of those vectors (multiplying the vectors by some weights/Scalars)
- We often want to determine if one or a couple vectors is in the span of a set $S$ of vectors
  - In this example, it is because you can multiply the vectors in the set $S$ by weights to get the vector $\textbf{v}$
  - It is a weighted combination of vectors in set $S$
  - The weights are not easy to find quickly and there are matrix operations for determining weights to see if a vector is a member of a set
    $$\textbf{v} = \begin{bmatrix}1 \\2 \\0\end{bmatrix} \space \textbf{w} = \begin{bmatrix}3 \\ 2 \\1\end{bmatrix} \quad S = \left\{ \begin{bmatrix}1 \\ 1 \\0\end{bmatrix},\begin{bmatrix}1 \\ 7 \\ 0\end{bmatrix}\right\}$$
    $$\textbf{v} \in \text{span}(S) \rightarrow \begin{bmatrix}1 \\ 2 \\0\end{bmatrix} = { 5 \over 6 } \begin{bmatrix}1 \\ 1 \\0\end{bmatrix} + {1 \over 6} \begin{bmatrix}1 \\ 7 \\ 0\end{bmatrix}$$
- Note: if the set has 0s in it and the vector we're trying to determine if it is in the set only has non-zero numbers, then we already know it is not in the span (see vector $\textbf{w}$ above - the third element 1 against the 0s in the span set)

#### Geometric Interpretation

- **The span of 2 independent vectors (not scaled versions of each other which would just be on the same line 1D plane) is a 2 dimensional plane**

  - Any point on the plane (which extends infinitely in all directions) can be expressed as some linear scaling of the vectors in the span set.
    - Since other sets of vectors can be in the space, this means that multiple distinct sets of vectors can span the same space
  - See visualization of how spans represent a plane in [video](https://www.udemy.com/course/linear-algebra-theory-and-implementation/learn/lecture/10500416) at timestamp 9:35

- The span $S$ above is a two dimensional plane embedded in a 3 dimensional ambient space
- Vector $\textbf{v}$ is a line that is also in the plane of $S$
- vector $\textbf{w}$ is not in the same plane (points off in some other direction)
- The vectors $\textbf{v}$ and $\textbf{w}$ are independent (one cannot be constructed as some multiple of the other), therefore the form a 2-D plane (this may not always be the case if they are dependent and one is just a scaled version of the other - making it on the same line)
- See visualization in [video](https://www.udemy.com/course/linear-algebra-theory-and-implementation/learn/lecture/10500416) at timestamp 5:20
