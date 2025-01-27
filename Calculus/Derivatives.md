# Derivatives

See [Python Notebook](./derivatives.ipynb)

- The slope of the line of a function as the Limit of change approaches 0

### Note on Differentiation vs. Derivates

- Derivative: The instantaneous slopes (i.e. at each point)
- Differentiation: The process and the technique of getting the derivative

### Notation

- the Delta greek letter represents a change in some quantity:
  $$\Delta x \over \Delta y$$
  or it's lowecase variant:
  $$\delta x \over \delta y$$

## The Slope of a Line

- **A Ratio** of the distance along the y-axis between two points over the distance along the x-axis. That ratio is the **Slope**.
- The change in `y` (output) over the change in `x` (input)
  - How much the dependent variable $y$ changes given some change in the independent variable $x$
- A higher ratio/number means that the slope is steeper, a smaller ratio means that the slope is less steep and more gradual

### Line function

- A line expressed as a function is:
  $$f(x) = mx + b$$
- $m$ is the slope parameter and $b$ is the `Intercept`

#### The Intercept: Where the line crosses the y-axis when $x = 0$

- The Intercept is unimportant for the Derivative - we only care about the $m$ slope parameter

### Computing the Slope parameter $m$

- The change in the $y$ axis values normalized by the change in the $x$ axis values
  - Take the difference between the y-axis of 2 points on a line and divide it by the difference of the x-axis coordinates for those points
    $$m = {{y_2 - y_1} \over {x_2 - x_1}} = {\Delta y \over \Delta x}$$

### The slope as it relates to the Derivative

- If we continue to chop up a portion of a line between two points into smaller and smaller line segments to get the Limit as the distance on the x-axis between those segments goes to 0
- The distance between two points along the x-axis $\Delta x$ as it gets smaller and smaller arbitrarily close to $0$ without actually being $0$ (then we would have ${\Delta x \over \Delta y} = {0 \over 0}$)
- At the limit as the segments get smaller and smaller towards 0 length (but not 0), we have a **slope series** (i.e. a vector of slopes for each chopped up line segment) - this is the Derivative
  - The slope series becomes the derivative when the segments are so numerous that the distances between them is almost 0
