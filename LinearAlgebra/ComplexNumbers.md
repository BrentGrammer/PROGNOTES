# Complex Numbers

- See [Notebook](./complexnumbers.ipynb)

- Complex numbers extend the framework of a 1-D line of numbers (negative on the left, positive on the right), so that there is an added dimension (a 'y-axis' off the number line, for example), and numbers can exist somewhere on this 2-D plane as opposed to being a point on the 1-D number line.
- The x-axis on the real number line is called the **REAL AXIS** and the y-axis is called the **IMAGINARY AXIS**
- Complex numbers are used in signal processing, engineering, applied math, the Fourier Transform etc.
  - They make operations more efficient and have advantageous utility

### What is "Imaginary"?

- Comes from the **Imaginary Operator** $i$
  - No number times itself can be a negative number, so in theory that cannot exist
  - There still must be a way to solve the equation: $x^2 + 1 = 0$
  - NOTE: $j$ is used for $i$ in the engineering world because $i$ is used for Electrical Current by convention.
    $$i = \sqrt{-1}$$

### Coordinates

- Complex numbers can have coordinates similar to x-y coordinates on a Cartesian Plane
- The REAL part is the x-coordinate, and the IMAGINARY part is the Y coordinate
  - $( 2 \space 3i )$ is a complex number with 2 on the x-axis and 3 on the y-axis

### Extra Information on Complex Numbers

- **MAGNITUDE** - The distance of the complex number on the plane from the Origin (0,0 coordinates)
  - In addition to an x and y axis coordinate, they also have a Magnitude distance from origin.
- **ANGLE** relative to the positive REAL axis (the x-axis)
- These can be extracted via Trigonometry.
- Can be characterized as a VECTOR
  - The first REAL part corresponds to the first element of a 2-D vector
  - The second IMAGINARY component in the number corresponds to the 2nd element in a 2-D vector

### The Set of Complex Numbers

- Complex Numbers are not members of the REAL set of numbers, they are members of the Complex set $\mathbb{C}$
  $$z = a + bi \in \mathbb{C}$$

## Multiplying Complex Numbers

- Use the FOIL method (Multiple Firsts, Outers, Inners and Lasts in the terms)

$$z = a + bi$$
$$w = c + di$$

$$z \times w = (a + bi)(c + di)$$
$$= ac + adi + cbi + bdi^2$$

- Reduces to (since $i^2$ is -1):
  $$ac + adi + cbi - bd$$

## Complex Numbers in Vectors

$$\begin{pmatrix} 1 \space 3i \\ -2i \\ 4 \\ -5 \end{pmatrix} \space \in \mathbb{C}^4$$

### The Dot Product of Vectors with Complex Numbers

- The complex numbers are not two numbers, they are one number/element in the vector, so be careful not to treat the real/imaginary part separate

$$\begin{pmatrix} 1 \space 3i \\ -2i \\ 4 \\ -5 \end{pmatrix}^T \begin{pmatrix} 6 \space 2i \\ 8 \\ 3i \\ -5 \end{pmatrix}$$

$$= (1 \space 3i)(6 \space 2i) + -16i + 12i + 25$$
$$= 6 + 2i + 18i - 6 -16i + 12i + 25$$
$$= 25 + 16i$$

## Hermitian Transpose (a.k.a. "Conjugate Transpose")

- Useful for computing the Dot Product of vectors that have Complex Numbers
- Often what is used to transpose complex vectors/matrices
- Takes into account an operation on Complex Numbers called the Complex Conjugate

### The Complex Conjugate of a Complex Number

- Flip the sign of the IMAGINARY part of a Complex Number without changing the REAL part of the Complex Number.
  - We're not changing the Magnitude of the Complex part, just it's sign

$$a \space {+bi} \rightarrow a \space{-bi}$$
$$a \space {-bi} \rightarrow a \space {+bi}$$

### Geometric Interpretation of the Complex Conjugate

- Flip the number across to the opposite side of the REAL number axis (x-axis) on the Complex Plan (x-y plane)
- NOTE: If the complex number is sitting directly on the REAL axis (the IMAGINARY part is 0), then the Complex Conjugate does NOTHING to the position of it on the complex plane.

### Hermitian Transpose:

- Use a captial $H$ or a star $*$ in place of the $T$
- Just like the regular Transpose, but any Imaginary numbers get their IMAGINARY components flipped in sign
  - Transposed means taking the column vector and transposing it into a row while flipping the imaginary signs:
    $$\begin{pmatrix} 1 \space 3i \\ -2i \\ 4 \\ -5 \end{pmatrix}^H = \begin{pmatrix} 1 \space 3i \\ -2i \\ 4 \\ -5 \end{pmatrix}^* = \begin{bmatrix} {1 \space 3i}, \space  +2i, \space  4, \space  -5 \end{bmatrix}$$

### Why We Need the Hermitian Transpose

- Trying to get the length of a vector to the origin, for ex., using a regular transpose (the magnitude of the vector times itself) generates an unintuitive and difficult result to work with using complex numbers
  - see [video explanation](https://www.udemy.com/course/linear-algebra-theory-and-implementation/learn/lecture/10992922) at timestamp 4:47

$$z^Tz = (\begin{bmatrix}3 \space 4i \end{bmatrix})(\begin{bmatrix}3 \space 4i \end{bmatrix}) = -7 + 24i \space \text{(Not easy to work with geometrically as a vector length result)}$$
$$z^Hz = (\begin{bmatrix}3 \space 4i \end{bmatrix})(\begin{bmatrix}3 \space -4i \end{bmatrix}) = 25 \space \text{(simpler result, more intuitive geomtric length)}$$
