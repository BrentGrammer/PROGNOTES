# Matrices

### Notation

- Use a capital bold letter symbol to represent a matrix
  $$\textbf{A} = \begin{bmatrix}1 & 6 & 0 \\ 7 & 2 & 4 \\4 & 1 & 1 \end{bmatrix}$$
- Use a lower case letter with the row and column in the subscript
  $$a_{1,2} = 6$$

#### Block Matrices

- Useful for notating large matrices and can offer some computational benefits
- Seperate parts of a matrix that become their own matrix
  - You can concatenate a representation of blocks:
    $$\textbf{A} = \begin{bmatrix}\textbf{D} & \textbf{0} \\ \textbf{1} & \textbf{D} \end{bmatrix} = \begin{bmatrix}3 & 0 & 0 & 0 \\0 & 4 & 0 & 0 \\1 & 1 & 3 & 0 \\1 & 1 & 0 & 4 \end{bmatrix}$$
    $$\textbf{D} = \begin{bmatrix}3 & 0 \\ 0 & 4 \end{bmatrix} \quad \textbf{0} = \begin{bmatrix}0 & 0 \\ 0 & 0 \end{bmatrix} \quad \textbf{1} = \begin{bmatrix}1 & 1 \\ 1 & 1 \end{bmatrix}$$

#### Diagonal Elements

- Start from the top left element and goes to the lower right
- All other elements are called **Off-diagonal Elements**
  $$\begin{bmatrix}1 & 0 & 0 & 0 \\0 & 1 & 0 & 0 \\0 & 0 & 1 & 0 \\0 & 0 & 0 & 1 \end{bmatrix}$$
- Note: Diagonals do not have to go all the way down to the bottom right, for example in a rectangular matrix, a diagonal just goes to the bottom row somewhere

#### Rows by Columns

- Refer to the shape of a matrix as rows x columns, ex: 4x3 matrix (4 rows, 3 columns)
- $m$ and $n$ are typical symbols used for rows by columns

### Dimensionality in Matrices

Can be interpreted in multiple ways in matrices (unlike vectors):

- The total number of elements (M x N): $\mathbb{R}^{MN}$
  - Note in this interpretation both a 2x3 and a 3x2 matrix would have a dimension of 6
- The space of M by N matrices: $\mathbb{R}^{M \times N}$
  - In this interpretation, a 2x3 matrix has a separate and completely different dimensionality than a 3x2 matrix
- Collection of Column Vectors: $C(\textbf{M}) \in \mathbb{R}^M$
  - The Column space of the matrix is in the set of R^M (M columns, so each of those column vectors has dimensionality of M)
  - The col space is the subspace spanned by the column vectors in the matrix
- Collection of Row Vectors: $R(\textbf{M}) \in \mathbb{R}^N$
  - The Row space of the matrix is in the set of R^N (N rows, so each of those row vectors has dimensionality of N)

#### Tensors

- Higher dimension matrices: MxNxK (i.e. in cube space)

### Types of Matrices

#### Square Matrix

- Has same number of rows as columns: MxM

#### Rectangular Matrix

- Non-square. MxN where $M \neq N$

#### Symmetric Matrix

- The elements on either side of the diagonal are the same (-1, 0, -4 below) and mirrored across the diagonal
- Only Square Matrices can be symmetric!
- the diagonal can consist of any elements/numbers - those elements mirror themselves
  $$\begin{bmatrix}1 & -1 & 0 \\-1 & -2 & -4 \\ 0 & -4 & 0 \end{bmatrix}$$

#### Skew-symmetric Matrix

- Similar to symmetric matrices, but you flip the sign on either side of the elements around the diagonal
- The diagonal must mirror it's sign, so the diagonal has to be 0s!
  $$\begin{bmatrix}0 & +1 & -2 \\-1 & 0 & -4 \\ +2 & +4 & 0 \end{bmatrix}$$

#### Identity Matrix

- All 1s on the diagonal and all 0s on the off-diagonal elements
- Is the matrix equivalent of the number $1$ - Any matrix or vector multiplied by the Identity Matrix is the same vector/matrix
- Always a square and symmetrical matrix, notated as $\textbf{I}$ with a subscript for the size
  $$\textbf{I}_3 = \begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}$$

#### Zero Matrix

- All zeros
- Any vector/matrix multiplied by the zero matrix is the zero matrix
- Notated with a bold $\textbf{0}$

#### Diagonal Matrix

- All zeros on the off-diagonal elements (note that the diagonal could have zero elements)
  $$\begin{bmatrix}1 & 0 & 0 \\ 0 & -2 & 0 \\ 0 & 0 & 5 \end{bmatrix}$$
- You can also have a diagonal rectangular matrix:
  $$\begin{bmatrix} \pi & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 5 & 0 \end{bmatrix}$$
- If all diagonal elements are the same, it can be written as a scalar of the Identity Matrix:
  $$\begin{bmatrix}2 & 0 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 2 \end{bmatrix} = 2{\textbf{I}}$$

#### Triangular Matrix
- Upper Triangular - all elements below the diagonal are 0
$$\begin{bmatrix}1 & 4 & 7 \\ 0 & -2 & 2 \\ 0 & 0 & 5 \end{bmatrix}$$
- Lower Triangular - all elements above the diagonal must be 0s
$$\begin{bmatrix} 1 & 0 & 0 & 0 \\ 3 & -2 & 0 & 0 \\ 4 & 5 & 5 & 0 \\ 1 & 2 & 7 & 4\end{bmatrix}$$

#### Concatenated Matrices
- Matrices must have the same number of rows to be concatenated
$$\begin{bmatrix} 1 & 4 & 2 \\ 3 & 1 & 9 \\ 4 & 2 & 0 \end{bmatrix} \sqcup \begin{bmatrix}7 & 2 \\ 7 & 2 \\ 7 & 1 \end{bmatrix} = \begin{bmatrix} 1 & 4 & 2 & \vert & 7 & 2 \\ 3 & 1 & 9 & \vert & 7 & 2 \\ 4 & 2 & 0 & \vert & 7 & 1 \end{bmatrix}$$