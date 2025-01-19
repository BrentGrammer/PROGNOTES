# Diagonal and trace

- Diagonal elements of a matrix can be extracted and placed into a vector
  - Ex: in Statistics the diagonal elements of a covariance matrix contain the variance of each variable.

### The Diag Function

- $\text{diag}$ as a function takes in a matrix as input and returns a vector as output

  - works on square and rectangular matrices to get the diagonal
  - Note: this is not the same thing as diagonalizing a matrix (eigendecomposition)

- The i-th element in vector v is the value at the i-th row and column of matrix A:
  $$\textbf{v}_i = \textbf{A}_{i,i}$$

### Computing Trace

- The sum of all of the diagonal elements
- used in computing some dot products and in normalizing values in eigendecomposition
- **Trace is only defined for SQUARE matrices and not Rectangular matrices**

- Trace is defined as the sum of all of the diagonal elements of a matrix A up to $m$ assuming a square matrix ($m$ = $n$)
  $$tr(\textbf{A}) = \sum_{i=1}^m \textbf{A}_{i,i}$$
