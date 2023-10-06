# Algorithms

### Binary Search

- Is the dataset you have ordered? if it is then there are advantages to this you can use
- This is O(logN) time (logarithmic time), ex. log(4096) = 12 -> you can halve 4096 twelve times to get to 1.
- continuosly halve the search space until you find the value - you never scan ( that would result in O(N) time)

#### Steps:

- Preqrequisite: The Array must be sorted! You can't do binary search on a nonsorted data set.
- to get the midpoint, take the low (start pos. of the array for ex) and add (entire length/2). \*Use the Math.floor of this result.
- check if value is the midpoint and return if found
- Check if value is larger than the midpoint (if v > midpoint), if yes then you search the right half of the data set
  - reset the low start pos. of the set to `low + 1`
- If val is less than midpoint, then reset the high to be the midpoint
  - Be careful of off by one errors - approach could be to think of the low as inclusive and the high position as exclusive
- loop over this algo while the low position is less than the high position (stop when they are at a crossing point, they always keep getting closer to each other on each iteration)

```javascript
function binarySearch(haystack, needle) {
  let low = 0;
  let high = haystack.length;

  do {
    const midpoint = Math.floor(low + (high - low) / 2);
    const value = haystack[midpoint];

    if (value === needle) {
      return true;
    } else if (value > needle) {
      high = midpoint; // high is exclusive, adjust to set it to the upper bound of the first half (lesser values)
    } else {
      // our val is less than the needle, we need to search on the right half/higher side
      low = midpoint + 1; // we want to drop the midpoint no need to look at it again.
    }
  } while (low < high); // note we do not want <= which would result in a off by one error since the high is not inclusive!
}
```

#### Crystal Ball Problem

- Given two crystal balls that will break if dropped from a high enough distance, determine the exact spot in which they will break in the most optimized way.
  - Example: You're in 100 story building, and you have two crystal balls and you wnat to find which floor they will break if dropped from it.
- Generalized problem: we have an array of Falses (point at which does not break) and we want to find at which point they start turning to a True value (the first point where you drop a ball and it breaks)
- To avoid linear search (jumping by half still results in linear time due to having a second ball and needing to go back to beginning??), and given this is a sorted data set (Falses, then Trues on the right), we can avoid linear searching, then change the unit of jumping to find the exact point of breakage. for instance, the square root of N. If we jump by this, and need to scan to find the exact point, at most we are scanning the square root of N so the op is O(sqrt(n))
  - If you jump by halfs (binary search), the worst case is that you have to walk half the array, whereby using sqrt(n) the worst case is walking sqrt(n) elements in the array.

```javascript
function twoCrystalBalls(breaks: boolean[]): number {
  // jump by the sqrt of N to avoid linear search (use divide and conquer approach)
  const jumpAmount = Math.floor(Math.sqrt(breaks.length));

  let i = jumpAmount;
  for (; i < breaks.length; i += jumpAmount) {
    // find point where it breaks then jump back sqrt(n) and walk forward sqrt(n)
    if (breaks[i]) {
      // check if we've entered the series of True points in the set
      break;
    }
  }

  i -= jumpAmount; // jump back sqrt N
  // we set j and make sure i is less than the entire set length in case we walk off the upper bound with the jump
  for (let j = 0; j < jumpAmount && i < breaks.length; ++j, ++i) {
    // if we find breaking point, return i
    if (breaks[i]) {
      return i;
    }
  }
  // not found
  return -1;
}
```

### Bubble Sort

- Sorting Property: x<sub>i</sub> <= x<sub>i+1</sub>
- Alogrithm:
  - Starts in 0th position, if i is larger than i+1 then swap positions, repeat up to the last position of the last iteration (see note below)
  - A singular iteration over a set of items will result in the largest item in the last position
  - each iteration over the set continues with one lest item until there is one item left - then it is sorted.
- Time complexity: O(n^2) - loop over set(or subset) for each N item in the set.
  - 1st iteration O(N), 2nd iteration: O(N-1), third iteration: O(N-2), ...O(N - N+1)

Note: accessing an array is constant time (O(1)), accessing a array twice is still constant time (it is two accesses, but we drop constants (2N === N))

Example:

```javascript
// Bubble sort is a sort in place algorithm
// loop up to N for each iteration (to not go out of the array, use n -1), inner loop is up to n - 1 - i

function bubbleSort(arr: number[]): void {
  // outer loop iterates over items in the set
  for (let i = 0; i < arr.length; i++) {
    // for each i go up to the next to last element of the last iteration, subtract i to exclude the last element (which will be highest in last position of last iteration)
    for (let j = 0; j < arr.length - 1 - i; j++) {
      // if current is greater than next, swap:
      if (arr[j] > arr[j + 1]) {
        // inner loop - subtract 1 so that you don't compare the last element to the next (non-existant) element and go outside of the list.
        // subtract i so that you also don't include iterating a comparison against the two last items of the last iteration - since the last item is always the highest sorted to end of iteration
        // could extract this into function
        // Note: this is constant time even though we access twice - array accessing is always O(1)
        const tmp = arr[j];
        arr[j] = arr[j + 1];
        arr[j + 1] = tmp;
      }
    }
  }
}
```

### Linked List

- Singly linked list: can't go backwards - only have a ref to the next node, and you lose the previous reference with each jump
- Doubly Linked List: you have a reference to the previous and next node.
- Different from a array in that it is a containerized list (the items are in containers that are heap allocated objects - stored in more expensive non-stack memory space)
- Deletions and Insertions in a Linked List can be very fast. Time complexity is O(1) - size of list does not affect the time of inserting N - we do the same constant amount of operations no matter how big the list is.
  - Order of operations is important when setting and deleting nodes in a linked list (if you remove a next pointer before you need to reference the next value, it is lost)

#### Time Complexity

**Main advantage of linked list is accessing/ops at either end of the list is very fast**
Main disadvantage is traversal is more expensive. Whenever you have a N lengthed algorithm, try to find another data structure.
Linked Lists make sense when you need things like Queues which require no traversal (just adding and popping from the tail/head)

- Getting head or tail of a linked list is special getters - they are O(1) constant operation since there is a pointer these locations
  - Same for deleting the head or tail
  - Prepending and appending is also O(1)
- Traversing or deleting from the inner elements of the list can be costly

#### Typical interface for a linked list:

```
interface LinkedList<T> {
  get length(): number;
  insertAt(item: T, index: number): void,
  remove(item: T): T | undefined;
  removeAt(index: number): T | undefined;
  append(item: T): void;
  prepend(item: T): void;
  get(index: number): T | undefined;
}
```

### Queue

- A specific implementation of a Linked List
- A queue is a FIFO structure
  - insertions start at the back/tail
    - You update the tail next to be the next item and set the tail = new item
  - popping starts at the start/head
    - ```
      h = head // save current head
      head = head.next
      h.next = null
      return h.val
      ```
- Note how this is a restricted linked list - it is a linked list that you can only use a certain way.

#### Time Complexity:

- O(1) -> There is no traversal, we just operate on the head and tail
- Interface: `enqueue`, `deque`, `peek`

```typescript
type Node<T> = {
  value: T;
  next?: Node<T>;
};

export default class Queue<T> {
  public length: number;
  private head?: Node<T>; // can be undefined
  private tail?: Node<T>;

  constructor() {
    this.head = this.tail = undefined; // initialize to undefined
    this.length = 0;
  }

  enqueue(item: T): void {
    const node = { value: item } as Node<T>;
    this.length++;
    // alternative could be to check if length of list is 0
    if (!this.tail) {
      // create the head (which is the tail) for an empty list
      this.tail = this.head = node;
      return;
    }

    this.tail.next = node; // update the current tail node next value to point to the newly added node
    this.tail = node; // update the tail position now with the newly added node
  }

  deque(): T | undefined {
    if (!this.head) {
      return undefined;
    }

    this.length--; // update the length prop to decrement

    const head = this.head; // save the head
    this.head = this.head.next; // update the head to be the next value in the queue

    // clear the tail if the list becomes empty at this point
    if (this.length === 0) {
      this.tail = undefined;
    }

    return head.value; // returns the original head
  }

  peek(): T | undefined {
    // return head if defined, otherwise return undefined.
    return this.head?.value;
  }
}
```

### Stack

- The opposite of a Queue
- interface: `pop`, `push`, `peek`
- no need to work with the tail, just the head for pushing and popping
- also O(1) constant time operations (dealing with head and tail and not traversing)

```typescript
type Node<T> = {
  value: T;
  prev?: Node<T>; // can use previous here instead of next for easier reasoning about
};

export default class Stack<T> {
  public length: number;
  private head?: Node<T>;

  constructor() {
    this.head = undefined;
    this.length = Node<T>;
  }

  push(item: T): void {
    const node = { value: item } as Node<T>;

    this.length++;
    if (!this.head) {
      this.head = node;
    }

    // point the new node to the current head:
    node.prev = this.head;
    this.head = node;
  }

  pop(): T | undefined {
    // use math.max to avoid setting length to -1 if the stack is empty - set max of 0 or current len - 1
    this.length = Math.max(0, this.length - 1);

    if (this.length === 0) {
      const head = this.head;
      this.head = undefined;
      return head?.value; // remember that head could be undefined if list is empty and pop is called on it. need to protect against accessing an undefined head .value
    }

    const head = this.head; // save value pointed to by head;
    this.head = head.prev; // set the head to next thing in the stack (could be undefined if no more items)

    return head.value;
  }

  peek(): T | undefined {
    return this.head?.value;
  }
}
```

### Arrays vs. Linked Lists

- All ops on arrays are O(1) constant time
- Arrays require allocating memory up front (which may or may not be fully used), Linked Lists have more optimized memory usage (but cost is time complexity)
- Linked Lists cannot be binary searched (no hops to the middle, only traversing)
  - If you need to scan or hop into a list for random access, use an array
  - If you only need to work with the head or tail of a list, use a linked list
  - Example, limiting API requests to 5 at a time - you want a queue (linked list) not an array, because with the array you have to shift the indices around everytime you remove one and add to the list.

### ArrayLists

- goal is to allow array access with the ability to grow. ArrayLists have the dynamic capacity to grow as needed (Arrays do not grow and are of a set length).
- Key takeaway - operations on the head or tail of array lists are expensive due to having to shift evrything over, but traversing is O(1). Linked lists are better for that but bad at traversing.
- You have a capacity (maximum allowed elements) and a length (currently inserted elements) property
  - The capacity is set to an amount that does not use too much memory and will grow as needed and if needed.
- an array list uses an array as the foundation (instead of a node container for ex.) and allows for being able to do `push`, `pull`, `pop` etc. operations.
  - ex: pushing onto an array list just checks the length, is it in capacity limit? then add value to the list. this is O(1) constant time.
- `push` O(1)
  - when you `push` to a array list which has length === capacity:
  - can create a new array of some longer length
  - copy in values from original list to the new array, retaining length pointer but increasing capacity
- `enqueue` O(N) - array lists are bad at enqueue and deque operations
  - operation requires you to shift over all values one position to insert a new value at the beginning of the array list.
- `deque` O(N) - same problem of shifting everything as with enqueue.
- In JavaScript, an array is an array list under the hood.

#### Pros and cons

- Getting values is bad on linked lists, Removing/adding items at the front of a list is bad on Array Lists.
  - ex if you have a million items in a list and you need to add/remove from the front, then you need to know that Array Lists are not good for this and a linked list would be better (keeping in mind random access disadvantage).
- Array lists and linked lists are good for pushing or popping from the end of lists
- Array lists give you random access (different from linked lists) of O(1) constant time. But you can't remove from the front as well with Array Lists.

### Array Buffers (Ring Buffers)

- Similar to a array list except the head and tail are index based (not the first and last item in the list necessarily)
  - with a head and tail in the middle of a list, everything on either side of the head/tail is null
  - This solves the problem of inserting items at the front of a list without needing to shift everything else. We just move the index of head (or tail) +1 and clean up the previous item.
- `push`,`pop`,`shift`,`unshift` are all O(1) instead of O(N)
- If you go out of bounds when adding, you can swing around to the beginning of the list (outside and before the indexed head)
  - You can use the modulo operator to do this: `this.tail % length`
    - `tail at 10 % len of 12 == 2` so the tail becomes index 2.
  - \*When the tail exceeds the head you need to resize the list
  - this is where the term 'Ring' buffer comes from (you loop around to make the shape of a ring oor you "ring" around the list)
- Ring buffers maintain order: when you shift or unshift you're getting the element that was last added to the front or perhaps the first element added.
  - Implication is since you're only adding to the tail and removing from the front, you're just creating a queue that runs around the ring.
  - see full explanation at 3:00 in [this video](https://frontendmasters.com/courses/algorithms/arraybuffer/)

### Use Cases

- Flushing in general or operations where you want to release a bunch of operations.
  - you don't want something with a linear add or remove time (i.e. shifting/unshifting on an array list) if not flushing the entire data set.
- Run into use cases more on the backend than the frontend (unless you're writing a library).
- for ring buffers: log batcher that needs to batch and write logs. logs need to maintain order, but while you're writing logs, new logs can come in. You can flush the logs as the ring buffer keeps on running while it's doing it (??)
  - You don't write into memory that's being unused until your tail exceeds your head
- Kafka is basically a distributed queue (it deals with order but among a distributed system with multiple computers)

### Object Pools

- reuse objects to retain more efficient memory usage
- Example: a server with 10000 requests that create a user object for every single request
  - Instead of creating a new object for each one, reuse an object, set new values on it, use it for the service and hand it back to a pool (keeps memory from spiking and going up and down - keeps it consistent and efficient)

## Recursion

- Function calling itself
- Needs a base case to stop the recursion.
  - **Move everything needed for base case outside of the recursing. Don't check for base cases or when to stop inside the resurse step. Put it all at the beginning first**
- Can have three steps (useful in path finding algos):
  - pre: do something before recursing
  - recurse: do the recursion
  - post: do something after recursing before returning
    - i.e. log out a value after calling the recursive function on each pass

```javascript
function sum(n) {
  if (n === 0) return 0;
  if (n === 1) return 1;
  // recurse step with a pre-step of adding n
  const result = n + sum(n - 1);
  // post step of logging out the argument
  console.log(n);
  return result;
}
```

- Note: when the logs occur using n = 5 for example, they will be `1,2,3,4,5` (not 5-4-3-2-1 since you go back up the stack for the return values after recursing).
  - In recursion you do down the stack to set return addresses pointing to the previous call, and then back up the stack to send return values up to the previous calls

### Quick Sort

- Divide and Conquer (includes Merge Sort): to split your input into chunks and then go over those smaller subsets and solve things faster. Gets smaller and smaller to a fundamental unit
- pick an element `P` (for Pivot)
  - any element that is less than or equal to the Pivot element is put in the first position
  - everything on the left side becomes less than or equal to pivot and everything on the right is greater than Pivot.
  - Take the chunks between the Pivot and beginning and the Pivot and the end and repeat the process
    - Do not include the Pivot (everything around the pivot)
    - When you get to a empty array or only one item, everything is then sorted.
    - Note that the lo and hi (left and right ends) are both inclusive
- This algo sorts in place
- O(n^2) worst case runtime complexity
  - Quick sort does not always sort quickly depending on if the pivot is not in the middle etc.
  - If the list is reversed and the pivot is `1`
  - Ideal case would be O(nlogn) (pivot is in the center)

#### Implementation

- split into two main functions:
  - partition(): produces the pivot index and moves items to one side or the other
  - quicksort(): does the sorting, calls partition, gets the pivot, then recalls quicksort recursively and handles the base case and book keeping.

Example input: [9,3,7,4,69,420,42]

```javascript
function qs(arr: number[], lo: number, hi: number): void {
  // base case - if lo and hi positions meet
  if (lo >= hi) return;

  const pivotIdx = partition(arr, lo, hi);

  // repeat again for each side of the list, but don't include the pivot index on the repeat
  qs(arr, lo, pivotIdx - 1); // do left side of chunk, -1 for inclusive end positions (not including pivot)
  qs(arr, pivotIdx + 1, hi); // do the right part of the chunk not including pivot
}

// returns the pivot index, lo and hi are index positions for the current chunk
function partition(arr: number[], lo: number, hi: number): number {
  const pivot = arr[hi];

  let idx = lo - 1; // -1 to enable insertion into the first position of the chunk (which includes the actual lo idx)

  // walk up to not incl. the hi
  for (let i = lo; i < hi; i++) {
    // compare against the pivot to determine where to place the element
    if (arr[i] <= pivot) {
      // inc index as soon as you find something you need to swap - the first time will inc to the first position. Idx is a marker that says everything to the left of me is sorted
      idx++;
      // swap, move what is less than or equal to pivot to the left position.
      // Ex: [8,7,6,4,5] - 5 is pivot, we walk up to 4 (<=5) and swap 8 into 4s position and move 4 to 8s idx.
      const tmp = arr[i];
      arr[i] = arr[idx];
      arr[idx] = tmp;
    }
  }

  // inc idx one more time (if nothing found less than, the idx would become zero)
  idx++;
  // swap the pivot (in our impl the highest position in a chunk) to be the idx marked value so that it becomes the new pivot
  arr[hi] = arr[idx];
  // return the new pivot index position (in place of the original array)
  return idx;
}

export default function quicksort(arr: number[]) {
  qs(arr, 0, arr.length - 1); // end/hi is inclusive which is unusual in most algorithms
}
```
