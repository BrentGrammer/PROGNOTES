# Cross Product

- See [Notebook](./vectormultiplication.ipynb)
- Another way of multiplying vectors, but only works with 3-D vectors
- Not as common in machine learning usage, but for geometry and physics it can be used.

## Computation

- Only applicable with **3-Dimensional Vectors**
- Result product vector is another 3-D vector
- The formula has kind of a cross diagonal flow of multiplying the terms, but generally you'll need to look the formula up if not memorized since it is not very intuitive

$$\begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix} \times \begin{bmatrix} a \\ b \\ c \end{bmatrix} = \begin{pmatrix} 2c - 3b \\ 3a - 1c \\ 1b - 2a \end{pmatrix}$$

### Geometric Explanation of Cross Product

- Any two vectors can define a unique 2-D plane (euclidian geometric)
- The vector computed by the cross product is **orthogonal** to the plane
  - see [explanation visualization](https://www.udemy.com/course/linear-algebra-theory-and-implementation/learn/lecture/14169807) at timestamp 2:41
  - The cross product vector is at a right angle to the plane (going up for example on the z-axis)
  - Called the **Normal Vector** of the plane (you can define the 2-d plane with the normal vector in geometry)
