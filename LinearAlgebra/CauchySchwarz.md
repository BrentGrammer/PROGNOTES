# Cauchy-Schwarz Inequality

- [See Notebook for Proofs](./cauchyschwarz.ipynb)

## The formula

- The absolute value of the dot product between two vectors $a$ and $b$ is less than or equal to the multiplication of the vector magnitudes/norms (lengths - signified with double bars `||`) of the two vectors:
  $$|a^Tb| \leq ||a|| \space ||b||$$

## Proving Cuachy-Schwarz Inequality

### Use the geometric expression of the dot product

- Replace the dot product in the formula with the geometric
  expression
  - Move the abosulte value wrappers to the cosine since that is the only term that can be negative (the lengths a and b are always positive)
  - Note: The cosine is bound b/w -1 and 1, and it's absolute value is bound between 0 and 1
    $$\textbf{||a|| \space ||b|| \space |} \boldsymbol{\cos}(\boldsymbol{\theta_{ab}}) \textbf{|} \leq ||a|| \space ||b||$$
- Divide both sides by $||a|| \space ||b||$ and get 1 on the right side of the eq.
  - PROOF: since the abs val of cosine is bound between 0 and 1, and that is the only term left after the division, the left side being less than or equal to the right is proven.

#### When the Dot product is less than (not equal) or equal:

- The dot product is less than the product of the vector norms (lengths) whenever the angle between $a$ and $b$ vectors ($\boldsymbol{\theta_{ab}}$) is anything other than 0 or 180 degrees (i.e. 0 or pi radians)
  - **If the angle between vectors $a$ and $b$ is 0 or 180 degrees (0 or pi radians), then the cosine is equal to -1 (for pi rad./180 deg) or +1 (for 0 rad.) (it is then, +1 due to absolute value, which makes it equal to the right side when proved as above)**
- Another way of expressing this:
  - If vectors $a$ and $b$ form a linearly **independent set**, then the sides of the equation are not equal (becomes inequality expression where the left side is less than the right side)
  - If $a$ and $b$ form a **dependent set** (this means one vector is a scaled version of the other vector), then the sides of the eq. are equal to each other.
