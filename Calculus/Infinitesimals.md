# Infinitesimal

- A contraversial quantity which is nebulous and not precisely defined.
- Modern Calculus is based on Limits without the use of Infinitesimals
  - Originally used by Leibnitz and Newton for Calculus (the idea of a derivative was based on an infinitesimal change of x input to a function to determine the slope)
  - Replaced with Limits as numbers go to 0
  - Infinitesimals can still be used in Non-standard Calculus

### Definition

- A number ($\epsilon$) that is larger than 0 but smaller than $r$ where $r$ is any real number:
  $$0 < \epsilon < r$$
- The opposite of or the inverse of infinity
- Infinitely small or smaller than the smallest possible quantity you can think of while still being larger than 0 (smaller than ANY Real number)
- Not a Real number and does not exist on the Real number line
- Usually notated with Epsilon:
  $$\epsilon = {1 \over \infty}$$

### Different infinitesimals

- There are different infinitesimals, some larger than others
  $$\epsilon_1 + \epsilon_2 = \epsilon_3$$
- A squared infinitesimal is smaller than the infinitesimal being squared
  $$\epsilon^2 < \epsilon$$

### The problem with Infinitesimals

- There are an infinite number of real numbers
- Since an infinitesimal is not on the real number line it seems logically impossible to have it be less than any real number
- Infinitesimals on a curve (two points) cannot capture all of the curvature (in between the infinitesimal points) so there is always some error
  - Note: if the infinitesimals are so close on the curve then there is no slope on the curve/function

### In computers

- There is a value in python called `Epsilon` which is around 2.220446049250313e-16 (10 to the minus 16)
- Represents the smallest distance between two successive numbers
- A literal infinitesimal could be thought of as any number than is smaller than the smallest machine precision number
