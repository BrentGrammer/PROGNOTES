# The Outer Product

- Examples in [Notebook](./vectormultiplication.ipynb)

- Another way to multiply vectors (as opposed to the Dot Product, which is also called the "Inner Product")
  - Useful for thinking about matrix multiplication and eigen decomposition
- The result is a matrix (instead of a single number as with the Dot Product)
  - Transpose the second vector $W$ instead of the first as with dot product ($V^TW$)
- Assumes that both vectors are column vectors
- The vectors do not have to be of the same size or dimension

$$\textbf{V} \space \textbf{W}^T = N\text{x}M$$

## Computing the Outer Product

### The Columnar Perspective

- Can think of vector $V$ as a column and $W$ as row vector
- The outer product is each element in the column vector scaled by each element in the row vector on the right:
  - Note: if the vector on the right was a different dimension ($\begin{bmatrix}a \space b \space c \end{bmatrix}$), then you could still compute the outer product - the result would just be the column elements scaled by the three row vector scalars, $a$, $b$, $c$
    $$\begin{bmatrix} 1 \\ 0 \\ 2 \\ 5 \end{bmatrix} \begin{bmatrix} a \space b \space c \space d \end{bmatrix} = \begin{pmatrix} 1a \space 1b \space 1c \space 1d \\ 0a \space 0b \space 0c \space 0d \\ 2a \space 2b \space 2c \space 2d \\ 5a \space 5b \space 5c \space 5d \end{pmatrix}$$

### The Row Perspective

- Start the same way with $V$ as a column vector and $W$ as a transposed row vector
- Scale each row element with the columnar values (the result is exactly the same as the Columnar Perspective above, just a different way of looking at the computation)
  - Just think of taking each row value $a,b,c,d$ and scalar multiplying them be each columnar value
