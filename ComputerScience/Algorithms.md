# Algorithms

## General patterns and Cues:

If it’s an array then problems can be solved usually with two pointers, sliding windows etc.

Or heap + map if you see most/ least frequent

Trees/ maps can mean bfs dfs traversal etc.

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
  - Ideal case would be O(n*logn) (pivot is in the center)
  - NOT GOOD to use quick sort if you have sorted or almost sorted data (use insertion sort instead for ex.)
  - If data is random and not sorted, then quick sort is good
- O(1) Memory space since it sorts array in place.
  - This is an advantage over something like MergeSort which creates new items in memory.

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
  // idx is where we swap to when finding val <= pivot and is a marker says everything to left of me is sorted

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
  arr[idx] = pivot; // arr[hi] was stored in pivot already so it is saved there and we can reuse here for the swap
  // return the new pivot index position (in place of the original array)
  return idx;
}

export default function quicksort(arr: number[]) {
  qs(arr, 0, arr.length - 1); // end/hi is inclusive which is unusual in most algorithms
}
```

## Heap (a.k.a. a Priority Queue)

- A binary tree where every child and grandchild is smaller (a MaxHeap) or larger (MinHeap) than the current node
- Whevever a node is added or deleted we must adjust the tree
- No traversal of the tree when using heaps
- Heaps maintain a Weak Ordering (not perfectly ordered, but there is a rule at every point)
- A heap is always COMPLETE - there are always a left and right node and not just one with the other side empty. There are no gaps.

### Heap Condition

- The rule about the ordering, i.e. if a MinHeap, every node below must be larger or equal to.

### MinHeap

- The minimum item is the root
- Top value must be the smallest value (all children must be greater than it)

#### Adding to a minheap

- Check if node to add is smaller than the parent (start at the bottom of the tree).
- If node is smaller, then swap the parent with the node added.
- Repeat this swapping up the tree until the node being added is not smaller than parent

### MaxHeap

- The maximum item is the root

### Heapifying up or down

- We can bubble nodes up or down (comparing greater or less than parent values to decide whether to swap)

### Data Structure of a heap

- _There are no node structures_ with left and right vals to keep track of, the values can be listed in an array
- The formula for knowing what element in the array list is where in the heap is: $${\text{left child}} = 2(index) + 1$$ $${\text{right child}} = 2(index) + 2$$
  - This makes managing the tree much simpler than if dealing with node structures
- The nodes in a heap are numbered starting from the top and down to the left and then right (across the whole breadth/row of the tree). see [video](https://frontendmasters.com/courses/algorithms/heap/) at around 3:30
- To find the parent node, the formula is: $${\text{parent node}} = (i - 1) / 2$$
  - Note: use integer division or a floor operation on the result. i.e. 13 /2 = 6 (not 6.5)
- To get the end node, just get the last item in the queue
- Heaps are self balancing - we only remove or add where the length is and bubbling into correct position
- Heaps are useful for priorities (thread scheduling)

### Implementing a Heap

```javascript
export default class MinHeap {
  public length; // used for insertion and deletion - need to maintain
  private data; // list

  constructor() {
    this.length = 0;
    this.data = [];
  }

  // Runtime is O(logn) - since half of tree is in the bottom layer (the ordering allows us to divide and conquer)
  insert(value) {
    this.data[this.length] = value; // add to end of list
    this.heapifyUp(this.length) // move newly added val to correct place to follow ordering rules.
    // increment length tracking
    this.length++;
  }

  // Runtime is O(logn)
  // delete sometimes called poll or pop
  delete() {
    // check for empty
    if (this.length === 0) {
      return -1; // sentinel value
    }

    const out = this.data[0];
    this.length--; // decrement length
    // handle only one el in list (will be 0 after decrementing):
    if (this.length === 0) {
      this.data = [];
      return out;
    }

    // take head and get value, take last val in the array and put it into head's position, then bubble it down

    // set the head to put the last node at the top
    this.data[0] = this.data[this.length];
    // start heapifying down starting at the top
    this.heapifyDown(0);
    return out;
  }

  // when we do deletion we need to remove head el, take last el in array and put it in first position, then heapify it all down
  private heapifyDown(idx) {
    // base case
    if (idx >= this.length) {
      // we're at the end of the list, return
      return;
    }

    const lIdx = this.leftChild(idx);
    const rIdx = this.rightChild(idx);

    // base case 2
    if (lIdx >= this.length) {
      // end of list checking left so return
      return;
    }
    const leftVal = this.data[lIdx];
    const rightVal = this.data[rIdx];
    const val = this.data[idx];

    // the right value is the smallest and we are greater than that, we need to swap and heapify down (because the value is more and needs to be under the least value in this iteration)
    if (leftVal > rightVal && val > rightVal) {
      // swap
      this.data[idx] = rightVal;
      this.data[rIdx] = val;
      this.heapifyDown(rIdx); // pass in new right with our val
    } else if (rightVal > leftVal && val > leftVal) {
      this.data[idx] = leftVal;
      this.data[lIdx] = val; // swap with left
      this.heapifyDown(lIdx);
    }
  }

  private heapifyUp(idx) {
    // we keep looking at parent and stop when out of range or find a parent that is larger than us. since this is min heap if we're larger then we do not bubble up
    if (idx === 0) return; // can't heapify up from first node

    const p = this.parent(idx);
    const parentVal = this.data[p]; // val of parent
    const v = this.data[idx]; // current val

    if (parentVal > v) {
      // swap if parent is more than us and keep going until it's not
      this.data[idx] = parentVal; // move parent down
      this.data[p] = v; // move current value up to parent's position
      this.heapifyUp(p); // now repeat at the new p made
    }
  }

  // need 5 private functions to help us
  private parent(idx) {
    // returns num which is the index of the parent
    return Math.floor((idx-1 / 2)) // formula for finding parent using int division
  }

  private leftChild(idx) {
    return idx * 2 + 1; // formula for finding left child in the list
  }

  private rightChild(idx) {
    return idx * 2 + 2; // formula for finding right child in the list
  }
}

```

## Tries (pronounces "trees" as in Retreival Tree)

- If not a priority queue, then probably is a trie
- called a Trie tree (try tree) or a prefix tree or digital tree
- Used in things like Auto Complete (if you type an "a" what kind of results should be gotten back? etc.)
  - Can operate in O(1) time given the keys have a minimum/max length
- common in interviews with questions like "You are given a list of words and need to build an autocomplete"
- or a caching mechanism problem that involves a path which can vary at points
  - example: we have a path we want to cache in some sort of graph: `videos/:id/title`
  - `id` in the path can vary, so we would check if videos exists, does :id exist, does the title exist at the end of the path and return the retrieved match.

### Runtime

- Tries are constant time O(1) runtime complexity
- N (the input) in the case of tries is not the length of the string we're putting into the algorithm, N is the amount of nodes.
  - As we add more nodes, hundreds of words, does our lookup time change? No it does not.
  - it is O(height) of the tree, but height is usually bound by some maximum allowable value (the longest english word etc.)

### Structure of a Trie

- In a trie of words for example, each letter would be a node and when you traverse a series of nodes that make a real word, it will have a ASTERISK CHILD - a \* node indicating that you have found a real word.
  - alternatively some tries will have a `isWord` boolean flag on the last node of the word itself instead of a additional hanging star node (asterisk)

### Searching a trie

- You can do depth first or breadth first searches
- Example: someone types a "c" and we want to show words with c in them. We do a depth first search on the trie - Depth first search will always give alphabetical ordered matches. (pre-order traversal - as we see a word collect it in the found results)
  - We could also do a breadth first search
- In tries you can have a Score and Frequency to prioritize which words to retrieve.

### Inserting into a trie

- Iterative loop where we go to current node and walk to the end to see if we need to insert

```python
insertion(str):
  current = head

  for c in str:
    if current[c]: # if current has the character, we set current to the character
      current = current[c]
    else:
      # create a new node
      node = createNode()
      current[c] = node
      current = node

  current.isWord = True # flag to say it's the end of a word

isNode(isWordBool):
  return {isWord: isWordBool, children: []}
```

### Deletion

- Recursion is usfeful here
- You want to get to the point of the node FIRST and then in the post operation delete your way back up.
  - If you delete first, you lose the entire rest of the tree
- This involves a post traversal operation
