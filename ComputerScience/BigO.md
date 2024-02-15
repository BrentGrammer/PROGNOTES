# Big O Notation

- Big O grows with respect to input
- Basically look for loops and how you go over the input to determine the Big O of an algorithm
- We drop constants and consider worst case scenarios for Big O

Good link with ex.: https://stackoverflow.com/questions/1592649/examples-of-algorithms-which-has-o1-on-log-n-and-olog-n-complexities

- Constant - always takes same time no matter size of input

- Logarithmic - doubling input does not double amount of work - Searching. Binary search, reducing sets of data until you find your goal. You halve the input you have to search, but only need to look at one point at a time - eventually goes down to zero

- Linear - 1 unit of work more for each input added

- QuasiLinear - n log n - Slightly more than linear - Sorting. Merge Sort Quick Sort, Heap Sort. divide and conquer strategies. Halve the amount of space you need to search, but you need to search the whole space each time - go over n chars, halve how much you need to do then go over n chars and halve that, etc.

  - The log n is a little extra on top of O(N) since we pass through the list one time but sorting has a bit of runtime overhead.

- Quadratic - handshake problem - each new person has to shake everyone's hand in room

- Exponential - avoid

## Time Complexity

- Elementary operation, unit of work - something that does not take a lot of time - i.e. looking up a memory address, looking up an item in an array etc.
- defined as the number of times a particular instruction set is executed rather than the total time taken

- O(how many operations per input) - operation is the whole algo steps per input.

- **Constant Time O(1) -** Very few programs are O(1) time. Does not mean 1 thing is done, but that a constant amount of things is done even as the input grows. (inserting/deleting from an array for example)
- **Logarithmic Time O(log(n))** - Better than linear time - usually binary search and divide and conquery strategies
- **Linear Time O(n) -** Most optimal algorithms will be in a linear pass, or even a few linear passes O(k\*n).
- **Quasilinear Time O(n \* log(n))** - This is very common for sorting algorithms. Quicksort
- **Quadratic Time O(n^2):** Most brute-force solutions will require O(n^2) time or slower, like checking if you have everything on your shopping list in your trolley.
- **Exponential Time O(2^n)** - Common for brute-force like testing every numerical password combination.

\*\*\*Avoid quadratic time (double for loops)

## Examples:

### Logarigthmic time:

binary search. divide and conquer is logarithmic time

Logarithmic: How many times 2 is multiplied by itself to get x
log(x) = y (2^y == x)
-As x doubles, y only increases by 1, altertatively, increasing the exponent y by 1 doubles x. This means when x is huge, y is comparatively tiny to x.
i.e. 16 (2^4) is 2^3 (8) * 2.
log(4) = 2 (2^2)
log(8) = 3 (2^3)
As input increases and doubles in size - you only perform one extra operation
[...8 numbers] - binary search. log(8) = 3 (2^3) - you split the array 3 times and you're done.
*Am I eliminating half of the input at every step of my function? If so, then it is logarithmic time complexity (same for space complexity).

**Whenever you halve inputs in the op it is either O(LogN) - no scanning of input - or O(NLogN) time - in the case of scanning any input**

### Binary Search

if odd number of els, the bigger side is on the left and smaller is on the right (middle point skews left)

O(log(n)) time complexity

O(1) space complexity (if iterative solution)

Iterative solution is preferrable to recursive solution

Recursive solution has space complexity of O (log(n))

### Depth First Search Algorithm

Time Complexity: O(V + E) vertices and edges
Space Complexity: O (N)

use while loop (while stack.length).

add children to beginning of stack and pop off first, repeat

Use a stack

pop: `arr.shift()`

push: `arr.unshift()` (add to top of stack)

keep track of sibling (right) and child (left) by pushing them onto stack in order

while stack not empty, iterate

useful if going deep in tree and interested in parent child relationships

### Breadth first search Algorithm

Use a Queue (store queue variable and use `.shift()` to dequeue and `.push()` to enqueue children spread out of current node in iteration)

track nodes of tree at each level

while queue not empty iterate

useful if validating a binary search tree
