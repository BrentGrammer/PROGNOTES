# Blazingly Fast JavaScript

- From [course on Frontend Masters](https://frontendmasters.com/courses/blazingly-fast-js)

## Testing

### Step Ladder

- Step Ladder Testing: run multiple tests that gradually increase load on the application.
  - Enables you to see how the system behaves as load increases.

## Common Performance issues (causes)

- Creating Objects
- Promises
- Maps and Sets may not necessarily be faster than an array - "Use a contiguous representation unless there is a good rason not to." - Bjarne Stroustrup, Creator of C++
  - With smaller sets of data, arrays can outperform Sets for ex. if construcing, removing, deleting and adding elements (the memory in an array is contiguous which offers some advantages)
  - Sets start outperforming arrays when the dataset becomes larger

### Hot Spot Optimizing

- Finding areas that appear to be the slowest in the application.
- Can be effective, but also misleading (making you think you fixed the underlying problem when you didn't)

### Using the Chrome Inspector:

- use `--inspect`: --inspect is a built-in flag for Node.js that allows you to enable the Chrome Developer Tools Protocol inspector for debugging Node.js applications.
  - `node --inspect your_script.js` (use `tsc && node --inspect your_script.js` if using typescript)
  - go to `chrome://inspect` in the browser > `Dedicated DevTools for Node`
  - Go to `Performance` tab and hit record button for about 10 seconds. This shows a timespan graph of operations and you can zoom in on this.
    - Click on dark blue sections to select everything if zoomed in or need to de-select
  - Go to the `Bottom-Up` tab in the bottom half of devtools screen
    - Organizes function by name and which one took the most time. (see [video](https://frontendmasters.com/courses/blazingly-fast-js/inspecting-debugging-performance/) at timestamp 2:13 for explanation of self and total time)
      - Total Time: total time function appears in the chart graph (?)
      - Self Time: the time the function is actually executing without anything else included - the time there is blue area under the function and nothing else under it in the graph.
      - The way you read the time graph is that the flat tops (bottoms where functions have nothing under them but dark blue area) are where the time is being spent
  - see [video](https://frontendmasters.com/courses/blazingly-fast-js/inspecting-debugging-performance/) at timestamp 3:35
  - Note if you click on the file in the bottom-up tab you can get some more time information on parts of the code, but these might not be trustworthy(?).
