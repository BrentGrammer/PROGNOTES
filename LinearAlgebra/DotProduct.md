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

# Dot Product Geometry

- The product of the lengths of the two vectors scaled by (multiplied by) the cosine of the angle between those two vectors:
  $$\alpha = ||a|| \ ||b||\cos{(\theta_{ab})}$$

### Formula

- The cosine of the angle between two vectors scaled by the products of the lengths of the vectors
  - length of $|a|$ times length of $|b|$ times the cosine of angle theta ($\theta$) between the two vectors $a$ and $b$
  - Note the length notation is slightly different with single bars here instead of double bars
    $$\alpha = |a||b|\cos{(\theta_{ab})}$$

#### Solving for the Angle

- divide both sides by $|a||b|$ to get $a / |a||b| = \cos{(\theta_ab)}$
- Apply the inverse cosine to both sides to get theta angle: $\arccos{(a/|a||b|)} = \theta_ab$

  - Note: the cosine has to be between -1 and +1.
  - Lengths of vectors are strictly non-negative
  - The sign of the dot product is related to the relationship between two vectors
  - $|a|$ and $|b|$ are always gonig to be non-negative (0 or positive numbers)
  - The only thing in this formula that can be negative is the cosine of the angle between the two vectors
  - There are 4 categories of dot product signs based on the angle between the two vectors
    - If the angle between the two vectors is less than 90 degrees (less than pi / 2), then the two vectors meet at an acute angle (meeting at the their TAIL points)
      - The cosine of that angle, then must be positive (the cosine of an acute angle is positive)
      - This means that the dot product must be positive then.
      - **If you see a dot product between two vectors that is greater than 0, then that means the two vectors have an angle between them of less than 90 degrees**
      - **If the angle between vectors is obtuse (greater than 90 deg), then the cosine will be negative, and therefore the dot product will also be negative**
      - **If the angle between vectors is 90 deg (pi / 2), then the dot product is 0, because the cosine of 90 deg or pi/2 is 0**
        - **It does not matter how long the vectors are in length. If they meet at a right angle, then the dot product is necessarily 0!!**
        - This is called **Orthogonal**
      - If the vectors are in the same direction, then the angle is 0, and the cosine of 0 is 1, and the dot product reduces to the multiplication of the lengths of the two vectors
        - If the two vectors are the same, the dot product is the length x length (it's length squared), so then the length is the square root of the length
          - This is why the length of a vector is computed as the square root of the dot product of the vector with itself.
    - If the angle of the other vector is 180 deg (pi) pointed in the opposite direction, then the cosine of the angle between the vectors (180 deg) is -1
      - The dot product has a negative sign

- **Important thing to know is the relationship between the cosine of the angle between two vectors and the sine of the dot product between those two vectors**
  - vectors that meet at a right angle are orthogonal and have a dot product of zero. a'b=0 is one of the most important expressions in linear algebra, and is the foundation for myriad applications ranging from subspace projections to least-squares statistical modeling to eigenvalue decomposition and singular value decomposition.

### The Law of Cosines

- Proof that the algebraic and geometric expressions for the dot product are equivalent
- The law of cosines is similar to the pythagorean theorem in that it is about finding the length of C
  - Find the length of the other sides of the triangle a and b and the angle between them
  - **The law of cosines though, is about how to solve for C when we DON'T have a right triangle!**
- [Proving the Law of Cosines](https://www.udemy.com/course/linear-algebra-theory-and-implementation/learn/lecture/10500394) at timestamp 9:27
  - Can do this using the pythagorean theorem by dropping an artificial vertical perpendicular projection at the apex of the triangle to create sub right triangles.
    $$c^2 = a^2 + b^2 - 2ab\cos \theta$$
  - Consider if theta is 90 deg (pi /2), then the last term becomes zero and we just have the pythagorean theorem
    - The Pythagorean Theorem is a special case of the Law of Cosines

### The Algebraic vs. Geometric expression

- Algebraic expression of A transpose B is equal to the cosine of the angle between a and b, multiplied by the magnitudes of the two vectors
  $$a^Tb = \cos{(\theta_{ab})}||a|| \ ||b||$$

## Cauchy Schwarz Inequality

- Relationship of dot product to lengths of the vectors
- See [Cauchy Schwarz Inequality](./CauchySchwarz.md)
