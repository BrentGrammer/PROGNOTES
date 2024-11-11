# Trigonometry and Trig Functions

-[Python Notebook](./trigonometry.ipynb)

- Term is from the base words, 'Trigon' and 'Metry' (measurement) - "the measurement of a Trigon"
  - 'Trigon' - an old school term for a Triangle ('Tri' for three, 'gon' for shape, similar to 'hexagon' etc.)
  - Trogonometry specifically deals with RIGHT TRIANGLES (that have one 90 degree angle)

### Main goal of Trigonometry

- The main part of Trigonometry is characterizing the Angle of the Adjacent and the Hypotenuse (see [video](https://www.udemy.com/course/pycalc1_x/learn/lecture/33947210#notes) at timestamp 1:46)
- `Theta` - the angle of the Hypotenuse and the Adjacent of a Right Triangle (or one of the non-right angles on the triangle)

## Labels of the Right Triangle:

- Adjacent - The bottom horizontal edge of the right triangle
- Hypotenuse - The angled vertical edge of the right triangle
- Opposite - the straight vertical side of the right triangle

## Main Trig Functions/Formulas (Tangent, Cosin and Sin)

- The cosin of Theta angle is the length of the Adjacent divided by the length of the Hypotenuse:
  $$\cos(\theta) = {a \over h}$$

- Sin of Angle Theta is the length of the Opposite of the triangle divided by the Hypotenuse:
  $$\sin(\theta) = {o \over h}$$

- Tangent can be re-expressed as the ratio of Sin to Cosin:
  $$\tan(\theta) = {o \over a} = {\sin(\theta) \over \cos(\theta)}$$

- Trick to remembering the formulas: "soh-cah-toa"

### Sin and Cosin are Ratios (Unitless)

- The ratio is UNIT-LESS: The specific units of measurement (ft., inches, etc.) do NOT matter
- The Angle DOES have a unit: **Radians**

### Radians

- A Radian is a measure of the Angle in the lower corner of the triangle at the origin, coords 0,0 to the point on the Unit Circle
- Radians are an alternative measure to degrees:
  - 1 radian ≈ 57.3 degrees
  - pi radians (1 radian * 3.14...) = 180 degrees
  - 360 degrees = $2\pi$ Radians = A full circle
  - 90 degrees = $\pi \over 2$ Radians
- Goes from $0$ Radians to $2\pi$ Radians (for one full cycle around the Unit Circle)
- NOTE: Radians increase as you go COUNTER-CLOCKWISE around the unit circle (starting from the right most point on the circle at $0$ or $2\pi$ (360 deg)

### The Unit Circle

- A Circle with a Radius of 1
  - Used to measure Radians (place a triangle inside the Unit Circle)
  - The distance from any point on the circle to the origin (0,0 coordinate on a plane graph) is exactly 1
- Goes from 0 radians to $2\pi$ (for one full cycle around the Unit Circle)
  - see [video](https://www.udemy.com/course/pycalc1_x/learn/lecture/33947210#notes) at timestamp 3:15 for visual
  - Sometimes expressed as `-pi` to `+pi` to show a deviation from 0 radians (??)

### Translating Cosin and Sin to Wave Format (via the Unit Circle)

- Cosin and Sin to Wave form: takes into account the **Unit Circle** (has a radius of 1)
  - See [video](https://www.udemy.com/course/pycalc1_x/learn/lecture/33947210#notes) at timestamp 3:47
- Take the top point of the right triagle and move it along the Unit Circle circumference/perimeter: the Adjacent bottom horizontal length of the triangle side increases and decreases along the x axis as the triangle is stretched transformed as the top point is moved around the unit circle
  - **The length of the Adjacent (the bottom horizontal line of the triangle), or projection onto the x-axis is the Cosin**
  - **The projection onto the y-axis is the Sin**
  - The value is positive when the line (Adjacent) goes to the right on the X of the plane and negative when it goes to the left of origin
- The upper and lower bound of the Wave graph Y-Axis is 1 and -1 (full length of Adjacent to the right, and full length of Adjacent to the left on the plane)
  - The Cosin/Adjacent crosses through the origin (0) as the upper point of the triangle is moved around the Unit Circle
  - X-Axis on the Cosin/Sin Graph: Four main quadrants - Range is from $-2\pi$ to $2\pi$

#### The Cosin of the Angle (how many Radians) as you move around the Unit Circle corresponds to the projection onto the X-Axis\*\*

- See Video(https://www.udemy.com/course/pycalc1_x/learn/lecture/33947210) at timestamp 7:45

#### Sin is the projection onto the Y-Axis (same idea)\*\*

### How to Read the Cosin/Sin Graphs:

- Theta (the Angle in Radians) is on the X-Axis
- The Cosin or Sin of Theta is on the Y-Axis

### Even vs. Odd functions (Function Symmetry)

- The Wave Graphs of Sin and Cosin reveal some properties of the trig functions
- Cosin is an **Even** Function because it starts at 0 (Y-Axis) and drops off on either side equally
- Sin is an **Odd** Function because from 0 on the Y-Axis, the values go up on the right, and down on the left of that point

### Tangent is unbounded

- Note that the Sin and Cosin functions are bounded (-1 to 1), while the Tangent function is unbounded
  - The tangent function will have discontinuities that go to positive or negative infinity as Cosin approaches or drops from 0

## Trig Identities

- Important properties that exist in Trigonometry
- Example: $\cos(2\theta) = \cos^2(\theta) - \sin^2(\theta)$

### Important Trig Identity to Memorize:

$$\cos^2(\theta) + \sin^2(\theta) = 1$$

- The sum of the squared cosin and sin of the same Theta is equal to 1
- Reminder of the Euclidian Distance formula to find the distance between two X/Y coords (the square root of square of distances of X and Y points):
  $$h = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$$
  (Where $a = $ Adjacent, $o = $ Opposite, and $h = $ Hypotenuse):
- To prove the above Trig Identity, expand the formula exponents:
  $$({a \over h})^2 + ({o \over h})^2 = 1 \Rightarrow {a^2 \over h^2} + {o^2 \over h^2} = 1$$
  Same denominator, so combine them and this simplifies to:
  $${a^2 + o^2 \over h^2} = 1$$
  which simplifies to the Pythagorean Theorem:
  $$a^2 + o^2 = h^2$$
  And we assume that the Hypotenuse is 1 since we're dealing with a Unit Circle (all distances from point to origin are 1)
