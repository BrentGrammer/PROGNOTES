# Matrix Addition/Subtraction

- see [Notebook](./matrixadditionsubtraction.ipynb)

- Need to have same number of elements in both matrices
  - Add each corresponding elements together (1 + 0, 2 + 4, 3 + 4, 0 + 2)

$$\begin{bmatrix} 1 & 2 \\ 3 & 0 \end{bmatrix} + \begin{bmatrix}0 & 4 \\ 4 & 2 \end{bmatrix} = \begin{bmatrix}1 & 6 \\ 7 & 2 \end{bmatrix}$$

- Subtracting works the same way, just subtract the corresponding elements

- Commutative: $\textbf{A} + \textbf{B} = \textbf{B} + \textbf{A}$

- Associative: $\textbf{A} + (\textbf{B} + \textbf{C}) = (\text{A} + \textbf{B}) + C$

### Shifting Matrices

- Add a scaled version of the identity matrix onto a matrix
- Can only be done on a square matrix
- The off-diagonal elements remain unchanged, but the diagonal elements are changed

$$\begin{bmatrix}1 & 2 \\ 2 & 4\end{bmatrix} + 3 \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} = \begin{bmatrix} 4 & 2 \\ 2 & 7 \end{bmatrix}$$

$$\textbf{A} + \lambda \textbf{I} = \textbf{C}$$

### Geometric Interpretation of shifting

- Pushes a matrix away from being a plane towards being a sphere
- Shifting a matrix is a common way to regularize a matrix (to make it easier to work with in Machine Learning applications)
