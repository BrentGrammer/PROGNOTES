# Transposing Matrices

See [Notebook](./transposematrix.ipynb)

- Rows become columns, and columns become rows
  - Same as a row vector becoming a column vector or vice versa
  - can think about it as the **first row** becomes the first column or the **first column** becomes the first row
- The order of the elements does not change, only the orientation

$$\begin{bmatrix}1 & 5\\ 0 & 6 \\ 2 & 8 \\ 5 & 3 \\ -2 & 0 \end{bmatrix}^T = \begin{bmatrix} 1 & 0 & 2 & 5 & -2 \\ 5 & 6 & 8 & 3 & 0 \end{bmatrix}$$

- Transposing a matrix twice gives you back the original matrix before the transposition
  $$\textbf{A}^{TT} = \textbf{A}$$

### Formally defining Symmetric and Skew-symmetric Matrices:

- A symmetric Matrix is one that equals its transposed version: $\textbf{A} = \textbf{A}^T$
  - Each column in the matrix is the same as its corresponding row: ex. - the first column = the first row
  - Matrices must be the same size (square)
- A Skew-symmetric Matrix is one that equals its negative (multiplied by -1) transposed version: $\textbf{A} = -\textbf{A}^T$
  - The first column = the first row if you multiply that row by -1, the second col = the second row multipled by -1, etc...
