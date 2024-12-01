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
